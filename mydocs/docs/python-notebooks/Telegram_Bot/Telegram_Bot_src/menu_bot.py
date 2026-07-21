from telegram import Update # 匯入 Telegram Bot 更新物件
from telegram.ext import ( # 匯入 Telegram Bot 功能模組
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv # 匯入讀取 .env 工具
import os


# 載入 .env 內容
load_dotenv()
# 取得 Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")


# /menu 功能選單
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    顯示所有功能
    """

    await update.message.reply_text(
        "功能選單：\n"
        "/today - 今日任務\n"
        "/mood - 心情打卡\n"
        "/study - 讀書提醒\n"
        "/food - 吃什麼建議"
    )


# /today 今日任務
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    提醒今日重點
    """

    await update.message.reply_text(
        "今天建議先完成一件最重要的事。"
    )


# /mood 心情打卡
async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    給使用者一句鼓勵
    """

    await update.message.reply_text(
        "今天的你值得先被照顧，記得休息。"
    )


# /study 讀書提醒
async def study(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    提供讀書提醒
    """

    await update.message.reply_text(
        "先讀 25 分鐘，再休息 5 分鐘。"
    )


# /food 吃飯建議
async def food(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    提供餐點建議
    """

    await update.message.reply_text(
        "今天可以考慮便當、麵店或鍋貼。"
    )


# 主程式
def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/menu指令")
    
    # 建立 Bot 應用程式
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 加入 /menu 指令
    app.add_handler(CommandHandler("menu", menu))

    # 加入 /today 指令
    app.add_handler(CommandHandler("today", today))

    # 加入 /mood 指令
    app.add_handler(CommandHandler("mood", mood))

    # 加入 /study 指令
    app.add_handler(CommandHandler("study", study))

    # 加入 /food 指令
    app.add_handler(CommandHandler("food", food))

    # 啟動 Bot
    app.run_polling()

    


# 程式進入點
if __name__ == "__main__":
    main()