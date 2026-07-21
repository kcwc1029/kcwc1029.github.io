from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import json
import os


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = Path("checkin_records.json")


def load_records():
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_records(records):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def get_now_time():
    return datetime.now().strftime("%H:%M:%S")


def get_user_name(update: Update):
    user = update.effective_user

    if user.username:
        return f"@{user.username}"

    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    if full_name:
        return full_name

    return "未知使用者"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用打卡簽到 Bot！\n\n"
        "你可以輸入：\n"
        "/checkin - 我要簽到\n"
        "/rank - 查看今日排名\n"
        "/me - 查看我的簽到狀態\n\n"
        "也可以直接輸入：\n"
        "簽到\n"
        "打卡\n"
        "今日排名\n"
        "我簽到了嗎"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "打卡簽到 Bot 使用說明\n\n"
        "每個人每天只能簽到一次。\n"
        "簽到後會記錄你的名稱、日期、時間，並存進 JSON 檔案。\n\n"
        "可用指令：\n"
        "/checkin - 簽到\n"
        "/rank - 查看今日簽到排名\n"
        "/me - 查看自己的簽到狀態"
    )


async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    records = load_records()

    today = get_today()
    now_time = get_now_time()

    # 以傳訊息的那個 Telegram 帳號去做簽道
    user_id = str(update.effective_user.id)
    user_name = get_user_name(update)

    if today not in records:
        records[today] = []

    for record in records[today]:
        if record["user_id"] == user_id:
            await update.message.reply_text(
                f"你今天已經簽到過囉！\n\n"
                f"簽到時間：{record['time']}"
            )
            return

    new_record = {
        "user_id": user_id,
        "name": user_name,
        "time": now_time
    }

    records[today].append(new_record)
    save_records(records)

    rank = len(records[today])

    await update.message.reply_text(
        f"簽到成功！\n\n"
        f"姓名：{user_name}\n"
        f"日期：{today}\n"
        f"時間：{now_time}\n"
        f"今日排名：第 {rank} 名"
    )


async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    records = load_records()
    today = get_today()

    if today not in records or len(records[today]) == 0:
        await update.message.reply_text(
            "今天還沒有人簽到。\n\n"
            "你可以輸入 /checkin 成為第一名。"
        )
        return

    today_records = sorted(records[today], key=lambda item: item["time"])

    lines = []

    for index, record in enumerate(today_records, start=1):
        lines.append(
            f"第 {index} 名：{record['name']}，{record['time']}"
        )

    reply = (
        f"今日簽到排名\n"
        f"日期：{today}\n\n"
        + "\n".join(lines)
    )

    await update.message.reply_text(reply)


async def me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    records = load_records()
    today = get_today()

    user_id = str(update.effective_user.id)

    if today not in records:
        await update.message.reply_text(
            "你今天還沒有簽到。\n\n"
            "可以輸入 /checkin 完成簽到。"
        )
        return

    for index, record in enumerate(records[today], start=1):
        if record["user_id"] == user_id:
            await update.message.reply_text(
                f"你今天已經簽到囉！\n\n"
                f"日期：{today}\n"
                f"時間：{record['time']}\n"
                f"今日排名：第 {index} 名"
            )
            return

    await update.message.reply_text(
        "你今天還沒有簽到。\n\n"
        "可以輸入 /checkin 完成簽到。"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    if "簽到" in text or "打卡" in text:
        await checkin(update, context)

    elif "排名" in text or "排行榜" in text:
        await rank(update, context)

    elif "我簽到了嗎" in text or "我的狀態" in text or "簽到狀態" in text:
        await me(update, context)

    else:
        await update.message.reply_text(
            "我看不太懂你的意思。\n\n"
            "你可以輸入：\n"
            "簽到\n"
            "今日排名\n"
            "我簽到了嗎\n\n"
            "或使用指令：\n"
            "/checkin\n"
            "/rank\n"
            "/me"
        )


def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/help指令")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("me", me))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()