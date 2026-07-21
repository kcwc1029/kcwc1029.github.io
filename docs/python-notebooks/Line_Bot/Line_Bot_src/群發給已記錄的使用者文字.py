import os
import json
from pathlib import Path

from dotenv import load_dotenv
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)


load_dotenv()

USERS_FILE = Path("../Line_Bot_datasets/users.json")

configuration = Configuration(
    access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
)


def load_users():
    if not USERS_FILE.exists():
        print("找不到 users.json")
        return []

    with USERS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def send_message(user_id, text):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[
                    TextMessage(text=text)
                ]
            )
        )


def send_all(text):
    users = load_users()

    if not users:
        print("目前沒有任何使用者")
        return

    success_count = 0
    fail_count = 0

    for user_id in users:
        try:
            send_message(user_id, text)
            print(f"發送成功：{user_id}")
            success_count += 1

        except Exception as error:
            print(f"發送失敗：{user_id}")
            print(error)
            fail_count += 1

    print("-" * 30)
    print(f"成功：{success_count}")
    print(f"失敗：{fail_count}")


if __name__ == "__main__":
    # message = input("請輸入要群發的文字：").strip()
    message = "呼阿"
    if not message:
        print("訊息不可以空白")
    else:
        send_all(message)