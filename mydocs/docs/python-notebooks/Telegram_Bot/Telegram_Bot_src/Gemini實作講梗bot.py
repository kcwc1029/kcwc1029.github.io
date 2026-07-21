# 安裝套件：
# uv add google-genai

from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from google import genai

from dotenv import load_dotenv

import os


load_dotenv() # 載入 .env 檔案

BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # 讀取 Gemini API Key

client = genai.Client(
    api_key=GEMINI_API_KEY
) # 建立 Gemini Client


# 呼叫 Gemini 產生中文笑話
def ask_gemini_joke(topic: str) -> str:

    prompt = f"""
        你是一位擅長中文幽默、梗圖風格與生活化笑話的創作者。

        請根據使用者提供的題材，產生一個中文梗或笑話。

        規則：
        1. 使用繁體中文
        2. 笑話要短，適合 Telegram 訊息
        3. 可以有諧音、反差、冷笑話或生活梗
        4. 不要解釋笑點
        5. 不要產生冒犯、歧視或成人內容

        題材：
        {topic}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt
    )

    return response.text # 回傳 Gemini 回覆內容


# /start 開始使用
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "歡迎使用 Gemini 中文笑話 Bot。\n\n"
        "你可以輸入：\n"
        "/joke 貓咪\n"
        "/joke 工程師\n"
        "/joke 期末考\n\n"
        "我會根據題材產生一個中文梗或笑話。"
    )


# /help 使用說明
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "Gemini 中文笑話 Bot 使用說明：\n\n"
        "/start - 開始使用 Bot\n"
        "/help - 查看使用說明\n"
        "/joke 題材 - 產生中文梗或笑話\n\n"
        "範例：\n"
        "/joke 貓咪\n"
        "/joke 程式設計\n"
        "/joke 上班族"
    )


# /joke 產生笑話
async def joke(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # 檢查是否輸入題材
    if not context.args:
        await update.message.reply_text(
            "用法：/joke 題材\n\n"
            "例如：/joke 工程師"
        )
        return

    topic = " ".join(context.args) # 組合題材文字

    await update.message.reply_text(
        "正在想一個中文梗，請稍候。"
    )

    # 呼叫 Gemini API
    try:
        joke_text = ask_gemini_joke(topic)

    except Exception as e:
        await update.message.reply_text(
            "呼叫 Gemini API 時發生錯誤，請稍後再試。\n\n"
            f"錯誤訊息：{e}"
        )
        return

    await update.message.reply_text(joke_text)


# 主程式
def main() -> None:

    # 檢查 BOT_TOKEN
    if not BOT_TOKEN:
        raise ValueError(
            "找不到 BOT_TOKEN，請確認 .env 是否設定正確。"
        )

    # 檢查 GEMINI_API_KEY
    if not GEMINI_API_KEY:
        raise ValueError(
            "找不到 GEMINI_API_KEY，請確認 .env 是否設定正確。"
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", joke))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()