import os

from dotenv import load_dotenv
from flask import Flask, abort, request

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

# 載入 .env
load_dotenv()

# Flask App
app = Flask(__name__)

# LINE 設定
configuration = Configuration(
    access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
)

handler = WebhookHandler(
    os.environ["LINE_CHANNEL_SECRET"]
)


@app.post("/callback")
def callback():
    """LINE Webhook"""

    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """收到文字訊息"""

    # 使用者輸入內容
    user_text = event.message.text

    # LINE User ID
    user_id = event.source.user_id

    # 印在終端機
    print("=" * 50)
    print("收到訊息")
    print("內容：", user_text)
    print("User ID：", user_id)
    print("=" * 50)

    # 回覆內容
    reply_text = f"""你剛剛說：{user_text}
--------------------
你的 User ID：{user_id}
    """

    with ApiClient(configuration) as api_client:

        line_bot_api = MessagingApi(api_client)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text=reply_text
                    )
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