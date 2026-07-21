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
    ImageMessage,
)


load_dotenv()

# users.json 位置
USERS_FILE = Path("../Line_Bot_datasets/users.json")

# LINE 設定
configuration = Configuration(
    access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
)


def load_users():
    """讀取 users.json 裡面的 userId 清單"""

    if not USERS_FILE.exists():
        print("找不到 users.json")
        return []

    with USERS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def send_text_and_image(user_id, text, image_url):
    """發送文字 + 圖片給單一使用者"""

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[
                    TextMessage(
                        text=text
                    ),
                    ImageMessage(
                        original_content_url=image_url,
                        preview_image_url=image_url
                    ),
                ]
            )
        )


def send_all(text, image_url):
    """群發文字 + 圖片給 users.json 裡所有使用者"""

    users = load_users()

    if not users:
        print("目前沒有任何使用者")
        return

    success_count = 0
    fail_count = 0

    for user_id in users:
        try:
            send_text_and_image(
                user_id=user_id,
                text=text,
                image_url=image_url
            )

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

    message = "今天課程開始囉！這是一則文字 + 圖片推播"

    image_url = "https://i.pinimg.com/736x/07/91/06/0791065ffe87a8e3994b88d7cefc71dc.jpg"

    send_all(
        text=message,
        image_url=image_url
    )