# import csv
# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from flask import Flask, abort, request
# from linebot.v3 import WebhookHandler
# from linebot.v3.exceptions import InvalidSignatureError
# from linebot.v3.messaging import (
#     ApiClient,
#     Configuration,
#     MessagingApi,
#     ReplyMessageRequest,
#     TextMessage,
# )
# from linebot.v3.webhooks import MessageEvent, TextMessageContent

# load_dotenv()

# BASE_DIR = Path(__file__).resolve().parents[1]
# DATA_PATH = BASE_DIR / "Line_Bot_datasets" / "campus_questions.csv"

# app = Flask(__name__)
# configuration = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
# handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


# def load_questions():
#     with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as file:
#         return list(csv.DictReader(file))


# QUESTIONS = load_questions()


# def search_answer(user_text):
#     user_text = user_text.strip()
#     for row in QUESTIONS:
#         keywords = [word.strip() for word in row["keywords"].split("|")]
#         if any(keyword and keyword in user_text for keyword in keywords):
#             return f"【{row['category']}】\n{row['answer']}"
#     return "我找不到對應答案。你可以問：選課、宿舍、社團、打工、期中、圖書館。"


# @app.post("/callback")
# def callback():
#     signature = request.headers.get("X-Line-Signature", "")
#     body = request.get_data(as_text=True)
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return "OK"


# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_text_message(event):
#     reply_text = search_answer(event.message.text)
#     with ApiClient(configuration) as api_client:
#         MessagingApi(api_client).reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=reply_text)],
#             )
#         )


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)

# 請你參考上述程式碼，幫我製作一個「小北百貨線上購物 Showba Online Shop」的 Line Bot 

# 題材來源：
# 小北百貨線上購物
# https://shop.showba.com.tw
# 名稱：小北百貨線上購物 Showba Online Shop



# 請幫我產生兩份檔案：

# 1. Python 程式碼
# 檔案名稱：Line_Bot_src/showba_qa_bot.py

# 2. CSV 資料檔
# 檔案名稱：Line_Bot_datasets/showba_questions.csv

# CSV 欄位需求：
# 請建立以下欄位：
# category,keywords,answer

# CSV 內容請全部使用繁體中文。
# 請至少設計 18 筆資料。
# 主題要符合「小北百貨線上購物」的情境。

# CSV 類別可以包含：
# - 平台介紹
# - 商品查詢
# - 生活用品
# - 五金工具
# - 清潔用品
# - 廚房用品
# - 收納用品
# - 美妝個清
# - 會員服務
# - 購物流程
# - 付款方式
# - 配送服務
# - 退換貨
# - 發票問題
# - 優惠活動
# - 門市資訊
# - 客服聯絡
# - 常見問題

# 請注意：
# - 不要編造即時價格
# - 不要編造真實優惠活動日期
# - 不要保證庫存一定有
# - 回答要像客服，但要簡潔
# - 如果是會變動的資訊，請提醒使用者以官方網站公告為準
# - CSV 的 keywords 請用 | 分隔，例如：
#   商品|搜尋|找東西|有賣嗎

# 請輸出格式：
# 先給我 Python 完整程式碼。
# 再給我 CSV 完整內容。
# 最後給我建議資料夾結構與 .env 範例。

# 請確保程式碼可以直接複製貼上使用。