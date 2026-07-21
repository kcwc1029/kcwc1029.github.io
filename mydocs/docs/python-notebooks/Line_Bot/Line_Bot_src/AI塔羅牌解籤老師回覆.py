import os
from io import BytesIO

from dotenv import load_dotenv
from flask import Flask, abort, request
from PIL import Image

from google import genai

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError

from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    FollowEvent,
)


load_dotenv()

app = Flask(__name__)

configuration = Configuration(
    access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
)

handler = WebhookHandler(
    os.environ["LINE_CHANNEL_SECRET"]
)

gemini_client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

GEMINI_MODEL = "gemini-3.1-flash-lite"


TAROT_ROLE_PROMPT = """
你是一位 AI 塔羅牌解籤老師。

請用繁體中文回答。
語氣溫柔、直覺敏銳，但不要神棍化。
請根據牌面或使用者問題，給出生活化建議。

回答格式：
【目前狀態】
【牌面提醒】
【可以怎麼做】
【一句話提醒】

限制：
- 不要說絕對命運
- 不要恐嚇使用者
- 不做醫療、法律、投資決定
- 回答適合 LINE 閱讀
- 不超過 700 字
"""


def ask_gemini_text(user_text):
    prompt = f"""
{TAROT_ROLE_PROMPT}

使用者的問題：
{user_text}
"""

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text

    except Exception as error:
        print("Gemini 文字 API 發生錯誤：", error)
        return "抱歉，塔羅老師目前暫時無法解讀，請稍後再試一次。"


def ask_gemini_image(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))

        prompt = f"""
{TAROT_ROLE_PROMPT}

使用者傳來一張塔羅牌截圖。
請你觀察圖片中的塔羅牌、牌名、牌面元素、正逆位或牌陣位置。

如果圖片不清楚，請直接說「圖片有點不清楚」，
不要假裝百分百看懂。
"""

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                prompt,
                image
            ]
        )

        return response.text

    except Exception as error:
        print("Gemini 圖片 API 發生錯誤：", error)
        return "抱歉，這張圖片目前無法解讀。請換一張更清楚的塔羅牌截圖再試一次。"


def reply_text(reply_token, text):
    if len(text) > 1800:
        text = text[:1800] + "\n\n...(內容過長，已截斷)"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[
                    TextMessage(text=text)
                ]
            )
        )


def download_line_image(message_id):
    """LINE Bot SDK v3 下載圖片要用 MessagingApiBlob"""

    with ApiClient(configuration) as api_client:
        blob_api = MessagingApiBlob(api_client)

        image_content = blob_api.get_message_content(
            message_id=message_id
        )

        return image_content


@app.post("/callback")
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(FollowEvent)
def handle_follow(event):
    welcome_text = """
我是 AI 塔羅牌解籤老師。

你可以直接傳文字問題，例如：

・最近感情運勢如何？
・我跟他的關係會有進展嗎？
・我該不該主動聯絡？
・這份工作適合我嗎？

你也可以直接傳塔羅牌截圖，
我會試著幫你看牌面與解讀。
"""

    reply_text(
        reply_token=event.reply_token,
        text=welcome_text
    )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_text = event.message.text.strip()

    print("=" * 50)
    print("收到文字：", user_text)
    print("=" * 50)

    ai_reply = ask_gemini_text(user_text)

    reply_text(
        reply_token=event.reply_token,
        text=ai_reply
    )


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    print("=" * 50)
    print("收到圖片，開始下載與解讀")
    print("=" * 50)

    try:
        image_bytes = download_line_image(
            message_id=event.message.id
        )

        ai_reply = ask_gemini_image(
            image_bytes=image_bytes
        )

        reply_text(
            reply_token=event.reply_token,
            text=ai_reply
        )

    except Exception as error:
        print("處理 LINE 圖片時發生錯誤：", error)

        reply_text(
            reply_token=event.reply_token,
            text="抱歉，這張圖片讀取失敗，請重新傳一張清楚的塔羅牌截圖。"
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )