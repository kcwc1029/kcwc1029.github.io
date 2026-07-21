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
    QuickReply,
    QuickReplyItem,
    MessageAction,
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
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


def create_quick_reply():
    return QuickReply(
        items=[
            QuickReplyItem(
                action=MessageAction(
                    label="課程查詢",
                    text="課程查詢"
                )
            ),
            QuickReplyItem(
                action=MessageAction(
                    label="聯絡老師",
                    text="聯絡老師"
                )
            ),
            QuickReplyItem(
                action=MessageAction(
                    label="校園地圖",
                    text="校園地圖"
                )
            ),
        ]
    )


def reply_with_quick_reply(reply_token, text):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[
                    TextMessage(
                        text=text,
                        quick_reply=create_quick_reply()
                    )
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
    user_id = event.source.user_id

    print("新好友加入")
    print("User ID：", user_id)

    reply_with_quick_reply(
        reply_token=event.reply_token,
        text=f"""歡迎加入校園小幫手！

你的 User ID：
{user_id}

請選擇下方功能："""
    )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_text = event.message.text
    user_id = event.source.user_id

    print("=" * 50)
    print("收到訊息：", user_text)
    print("User ID：", user_id)
    print("=" * 50)

    if user_text == "課程查詢":
        reply_text = "目前課程包含：Python 入門、LINE Bot、AI 應用。"

    elif user_text == "聯絡老師":
        reply_text = "你可以透過 Email 或課堂群組聯絡老師。"

    elif user_text == "校園地圖":
        reply_text = "校園地圖連結：https://www.google.com/maps"

    else:
        reply_text = f"""你剛剛說：{user_text}
請選擇下方功能："""

    reply_with_quick_reply(
        reply_token=event.reply_token,
        text=reply_text
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )