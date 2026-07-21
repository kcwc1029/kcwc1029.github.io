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


# 呼叫 Gemini 產生超商調酒推薦
def ask_gemini_wine(store_name: str) -> str:

    prompt = f"""
        你是一位台灣超商調酒推薦專家。

        請根據使用者輸入的超商名稱，
        推薦一款適合在該超商買得到材料的超商調酒。

        規則：
        1. 使用繁體中文
        2. 調酒材料要盡量能在台灣超商買到
        3. 內容包含：
           - 調酒名稱
           - 材料
           - 簡單做法
           - 風味描述
        4. 回覆簡短、像聊天
        5. 不要過度正式

        超商名稱：
        {store_name}
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
        "歡迎使用超商調酒推薦 Bot。\n\n"
        "你可以輸入：\n"
        "/wine 7-11\n"
        "/wine 全家\n"
        "/wine 萊爾富\n\n"
        "我會推薦你一款超商調酒。"
    )


# /help 使用說明
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "超商調酒推薦 Bot 使用說明：\n\n"
        "/start - 開始使用 Bot\n"
        "/help - 查看使用說明\n"
        "/wine 超商名稱 - 推薦超商調酒\n\n"
        "支援超商：\n"
        "7-11\n"
        "全家\n"
        "萊爾富\n\n"
        "範例：\n"
        "/wine 7-11"
    )


# /wine 推薦調酒
async def wine(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # 檢查是否輸入超商名稱
    if not context.args:
        await update.message.reply_text(
            "用法：/wine 超商名稱\n\n"
            "例如：/wine 全家"
        )
        return

    store_name = " ".join(context.args).strip()

    # 驗證超商名稱
    valid_stores = [
        "7-11",
        "全家",
        "萊爾富"
    ]

    if store_name not in valid_stores:
        await update.message.reply_text(
            "目前只支援：7-11、全家、萊爾富"
        )
        return

    await update.message.reply_text(
        "正在幫你調一杯超商調酒，請稍候。"
    )

    # 呼叫 Gemini API
    try:
        wine_text = ask_gemini_wine(store_name)

    except Exception as e:
        await update.message.reply_text(
            "呼叫 Gemini API 時發生錯誤，請稍後再試。\n\n"
            f"錯誤訊息：{e}"
        )
        return

    await update.message.reply_text(wine_text)


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
    app.add_handler(CommandHandler("wine", wine))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()