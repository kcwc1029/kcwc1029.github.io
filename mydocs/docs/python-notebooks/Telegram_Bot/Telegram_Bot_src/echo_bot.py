### 製作tg bot，使用者傳送文字，tg bot會再附覆誦一遍

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,   # 建立 Bot 應用程式
    CommandHandler,       # 處理 /start、/help 等指令
    MessageHandler,       # 處理一般文字訊息
    ContextTypes,         # 提供 context 物件型別
    filters,              # 過濾訊息類型
)


from dotenv import load_dotenv # 匯入讀取 .env 環境變數工具
import os # 匯入作業系統模組，用來取得環境變數

load_dotenv() # 載入 .env 檔案內容
BOT_TOKEN = os.getenv("BOT_TOKEN") # 從 .env 中讀取 BOT_TOKEN

# /start 指令功能
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    當使用者輸入 /start 時執行
    """
    await update.message.reply_text(
        "你好，我是你的第一個 Telegram Bot。\n"
        "你可以先輸入 /help 看功能。"
    )

# /help 指令功能
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    當使用者輸入 /help 時執行
    """
    await update.message.reply_text(
        "/start - 開始使用\n"
        "/help - 顯示指令說明\n"
        "直接傳文字給我，我會回傳相同內容"
    )

# 一般文字訊息功能
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    當使用者輸入一般文字時執行
    將使用者輸入內容原樣回傳
    """
    user_text = update.message.text
    await update.message.reply_text(f"你剛剛說：{user_text}")

# 建立 Bot 主程式
app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Telegram Bot 應用程式
app.add_handler(CommandHandler("start", start)) # 加入 /start 指令處理器
app.add_handler(CommandHandler("help", help_command)) # 加入 /help 指令處理器

# 加入一般文字訊息處理器
app.add_handler( # 只接收文字，排除指令訊息
    MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
)

app.run_polling() # 啟動 Bot（輪詢模式）