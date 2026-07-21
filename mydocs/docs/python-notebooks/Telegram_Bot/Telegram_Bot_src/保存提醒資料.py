
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv
import os
import time


load_dotenv() # 載入 .env 檔案
BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token


# 暫存使用者提醒資料
USER_REMINDERS: dict[str, dict[str, str]] = {}


# /help 使用說明
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "讀書提醒 Bot 使用流程：\n\n"
        "1. 使用 /remind 分鐘 內容 建立提醒\n"
        "2. 使用 /reminders 查看目前尚未觸發的提醒\n"
        "3. 使用 /cancel 編號 取消指定提醒\n\n"
        "範例：\n"
        "/remind 25 讀作業系統\n"
        "/reminders\n"
        "/cancel 1\n\n"
        "指令列表：\n"
        "/help：查看使用說明\n"
        "/remind：建立提醒\n"
        "/reminders：查看提醒\n"
        "/cancel：取消提醒"
    )


# /remind 建立提醒
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # 檢查指令格式
    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text(
            "用法：/remind 分鐘 內容"
        )
        return

    minutes = int(context.args[0]) # 取得分鐘數
    content = " ".join(context.args[1:]) # 組合提醒內容

    user_id = str(update.effective_user.id)

    # 建立唯一工作名稱
    job_name = f"study_{user_id}_{int(time.time())}"

    # 建立提醒排程
    context.job_queue.run_once(
        fire_reminder,
        when=minutes * 60, # 分鐘轉秒數
        chat_id=update.effective_chat.id,
        name=job_name,
        data={
            "content": content,
            "user_id": user_id,
            "job_name": job_name
        },
    )

    # 儲存提醒資料
    USER_REMINDERS.setdefault(user_id, {})[job_name] = content

    await update.message.reply_text(
        f"已設定提醒：{minutes} 分鐘後提醒你 {content}"
    )


# 到時間後發送提醒
async def fire_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    data = context.job.data

    user_id = data["user_id"]
    job_name = data["job_name"]

    # 移除已完成提醒
    USER_REMINDERS.get(user_id, {}).pop(job_name, None)

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f"讀書提醒：{data['content']}"
    )


# /reminders 查看提醒
async def reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)

    items = list(
        USER_REMINDERS.get(user_id, {}).values()
    )

    if not items:
        await update.message.reply_text(
            "目前沒有任何提醒。"
        )
        return

    lines = ["目前提醒："]

    for index, content in enumerate(items, start=1):
        lines.append(f"{index}. {content}")

    await update.message.reply_text(
        "\n".join(lines)
    )


# /cancel 取消提醒
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # 檢查取消編號
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "用法：/cancel 編號"
        )
        return

    user_id = str(update.effective_user.id)

    items = list(
        USER_REMINDERS.get(user_id, {}).items()
    )

    index = int(context.args[0]) - 1 # 轉成索引

    # 檢查索引範圍
    if index < 0 or index >= len(items):
        await update.message.reply_text(
            "找不到這個編號。"
        )
        return

    job_name, content = items[index]

    # 移除排程工作
    for job in context.job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()

    del USER_REMINDERS[user_id][job_name]

    await update.message.reply_text(
        f"已取消提醒：{content}"
    )


# 主程式
def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/help指令")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("reminders", reminders))
    app.add_handler(CommandHandler("cancel", cancel))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()
