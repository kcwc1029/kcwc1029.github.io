"""製作 tg bot，使用 JSON 製作台南旅遊景點推薦 Bot"""

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv
import json
import os


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "../Telegram_Bot_datasets/tainan_spots.json"


# 讀取 JSON 景點資料
def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用台南旅遊景點推薦 Bot。\n\n"
        "你可以輸入 /help 查看使用方式，\n"
        "或輸入 /areas 查看目前支援的台南區域。"
    )


# /help 使用說明
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "台南旅遊景點推薦 Bot 使用說明：\n\n"
        "/areas - 查看支援區域\n"
        "/recommend 區域 - 推薦該區景點\n"
        "/search 關鍵字 - 搜尋景點名稱、類型或介紹\n\n"
        "範例：\n"
        "/recommend 安平\n"
        "/recommend 中西區\n"
        "/search 古蹟\n"
        "/search 拍照"
    )


# /areas 查看所有區域
async def list_areas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = load_data()

    if not data:
        await update.message.reply_text("目前沒有景點資料。")
        return

    area_text = "目前支援的台南區域：\n\n"

    for area in data.keys():
        area_text += f"- {area}\n"

    area_text += "\n你可以輸入：/recommend 安平"

    await update.message.reply_text(area_text)


# /recommend 區域
async def recommend_spots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "請輸入想查詢的區域。\n\n"
            "例如：/recommend 安平"
        )
        return

    area = " ".join(context.args)
    data = load_data()

    if area not in data:
        await update.message.reply_text(
            f"目前沒有「{area}」的景點資料。\n\n"
            "你可以輸入 /areas 查看支援區域。"
        )
        return

    spots = data[area]

    reply_text = f"台南 {area} 景點推薦：\n\n"

    for index, spot in enumerate(spots, start=1):
        reply_text += (
            f"{index}. {spot['name']}\n"
            f"類型：{spot['type']}\n"
            f"介紹：{spot['description']}\n"
            f"適合時間：{spot['best_time']}\n"
            f"預算：{spot['budget']}\n\n"
        )

    await update.message.reply_text(reply_text)


# /search 關鍵字
async def search_spots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "請輸入搜尋關鍵字。\n\n"
            "例如：/search 古蹟"
        )
        return

    keyword = " ".join(context.args)
    data = load_data()

    results = []

    for area, spots in data.items():
        for spot in spots:
            search_text = (
                spot["name"]
                + spot["type"]
                + spot["description"]
                + spot["best_time"]
                + spot["budget"]
            )

            if keyword in search_text:
                results.append((area, spot))

    if not results:
        await update.message.reply_text(f"找不到和「{keyword}」相關的景點。")
        return

    reply_text = f"搜尋「{keyword}」的結果：\n\n"

    for index, (area, spot) in enumerate(results, start=1):
        reply_text += (
            f"{index}. {spot['name']} ({area})\n"
            f"類型：{spot['type']}\n"
            f"介紹：{spot['description']}\n"
            f"適合時間：{spot['best_time']}\n\n"
        )

    await update.message.reply_text(reply_text)


# 主程式
def main() -> None:
    print("台南旅遊景點推薦 Bot 啟用中")
    print("可以先輸入 /help 查看指令")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("areas", list_areas))
    app.add_handler(CommandHandler("recommend", recommend_spots))
    app.add_handler(CommandHandler("search", search_spots))

    app.run_polling()


if __name__ == "__main__":
    main()