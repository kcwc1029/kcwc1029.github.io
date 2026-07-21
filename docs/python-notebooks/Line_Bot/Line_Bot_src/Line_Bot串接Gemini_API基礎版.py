import os

from dotenv import load_dotenv
from flask import Flask, abort, request

from google import genai

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)


load_dotenv()

app = Flask(__name__)

# LINE 設定
configuration = Configuration(
    access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
)

handler = WebhookHandler(
    os.environ["LINE_CHANNEL_SECRET"]
)

# Gemini 設定
gemini_client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def ask_gemini(user_text):
    """把使用者訊息丟給 Gemini，取得 AI 回覆"""

    prompt = f"""
你是一個 LINE Bot AI 助手。
請用繁體中文回答。
回答要簡短、清楚、適合手機閱讀。

使用者說：
{user_text}
"""

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as error:
        print("Gemini API 發生錯誤：", error)
        return "抱歉，AI 目前暫時無法回覆，請稍後再試。"


@app.post("/callback")
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_text = event.message.text.strip()

    print("使用者訊息：", user_text)

    reply_text = ask_gemini(user_text)

    # LINE 單則文字訊息有長度限制，保守切短一點
    if len(reply_text) > 1800:
        reply_text = reply_text[:1800] + "\n\n...(內容過長，已截斷)"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=reply_text)
                ],
            )
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )