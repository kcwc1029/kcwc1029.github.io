import csv
import os
from pathlib import Path

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
from linebot.v3.webhooks import MessageEvent, TextMessageContent

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "Line_Bot_datasets" / "campus_questions.csv"

app = Flask(__name__)
configuration = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


def load_questions():
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


QUESTIONS = load_questions()

def search_answer(user_text):
    user_text = user_text.strip()
    for row in QUESTIONS:
        keywords = [word.strip() for word in row["keywords"].split("|")]
        if any(keyword and keyword in user_text for keyword in keywords):
            return f"【{row['category']}】\n{row['answer']}"
    return "我找不到對應答案。你可以問：選課、宿舍、社團、打工、期中、圖書館。"


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
    reply_text = search_answer(event.message.text)
    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
