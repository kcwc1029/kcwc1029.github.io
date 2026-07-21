from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv
import os


load_dotenv() # 載入 .env 檔案
BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token


# /help 使用說明
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "提醒 Bot 使用流程：\n\n"
        "1. 輸入 /remind 分鐘 內容\n"
        "2. 分鐘必須是整數\n"
        "3. 時間到後，Bot 會自動傳送提醒訊息\n\n"
        "範例：\n"
        "/remind 10 寫 Python 作業\n"
        "/remind 30 喝水休息\n\n"
        "其他指令：\n"
        "/help：查看使用說明"
    )


# /remind 設定提醒
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # 檢查參數是否足夠
    if len(context.args) < 2:
        await update.message.reply_text(
            "用法：/remind 分鐘 內容"
        )
        return

    # 驗證分鐘是否為整數
    if not context.args[0].isdigit():
        await update.message.reply_text(
            "分鐘必須是整數"
        )
        return

    minutes = int(context.args[0]) # 取得分鐘數
    content = " ".join(context.args[1:]) # 組合提醒內容

    # 建立提醒排程
    context.job_queue.run_once(
        send_reminder,
        when=minutes * 60, # 轉成秒數
        chat_id=update.effective_chat.id,
        data={
            "content": content
        },
    )

    await update.message.reply_text(
        f"已設定 {minutes} 分鐘後提醒：{content}"
    )


# 到時間後發送提醒
async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    content = context.job.data["content"] # 取得提醒內容

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f"提醒時間到：{content}"
    )


# 主程式
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("remind", remind)
    )

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()