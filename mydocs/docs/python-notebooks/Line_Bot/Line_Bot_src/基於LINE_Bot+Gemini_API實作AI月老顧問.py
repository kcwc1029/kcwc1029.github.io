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
    FollowEvent,
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
    """把使用者的感情問題交給 Gemini"""

    prompt = f"""
你現在是一位「AI 月老顧問」。

你的角色設定：
- 你擅長感情分析、曖昧判斷、聊天回覆建議、告白建議、分手後調適。
- 你的語氣像一位有經驗、溫柔但不灌雞湯的學長姐。
- 你會先理解使用者的情緒，再給具體建議。
- 你不要只說大道理，要給可以直接照做的回覆範例。
- 如果使用者問「我該怎麼回」，請直接提供 2 到 3 種可複製的聊天回覆。
- 如果情境不清楚，不要一直追問，先根據現有資訊給一個合理建議。
- 一律使用繁體中文。
- 回答適合手機閱讀。
- 回答不要超過 600 字。

安全限制：
- 不鼓勵控制、威脅、情緒勒索、跟蹤或騷擾。
- 如果使用者想傷害自己或他人，請溫和建議立刻找可信任的人或專業資源協助。

使用者的問題：
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
        return "抱歉，AI 月老目前暫時牽線失敗，請稍後再問我一次。"


def reply_message(reply_token, text):
    """回覆 LINE 訊息"""

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
    """使用者加入好友時，自動發送歡迎訊息"""

    welcome_text = """
我是 AI 月老顧問。

你可以問我：

・他這樣回，是不是對我有意思？
・我該怎麼開話題？
・曖昧對象突然變冷淡怎麼辦？
・告白前要注意什麼？
・我想回訊息，但不知道怎麼講

直接把你的狀況丟給我，我會幫你分析。
"""

    reply_message(
        reply_token=event.reply_token,
        text=welcome_text
    )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """使用者傳文字後，交給 Gemini 回覆"""

    user_text = event.message.text.strip()

    print("=" * 50)
    print("使用者問題：", user_text)
    print("=" * 50)

    ai_reply = ask_gemini(user_text)

    reply_message(
        reply_token=event.reply_token,
        text=ai_reply
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )