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


# 呼叫 Gemini 取得職涯建議
def ask_gemini_career_advice(user_input: str) -> str:

    prompt = f"""
        你是一位溫和、務實、具教育背景的職涯輔導顧問。

        請根據使用者的描述，提供「職涯導向輔導建議」。

        請用繁體中文回答，並依照以下格式：

        一、狀況理解：請先整理使用者目前的狀況。
        二、可能適合的方向：列出 2 到 4 個可能適合的職涯方向。
        三、需要培養的能力：列出具體能力，例如程式、資料分析、溝通、作品集、證照、實習等。
        四、接下來 30 天可以做什麼：給出具體、可執行的短期行動建議。
        五、提醒：請提醒使用者：這是職涯參考建議，不是絕對答案，仍需要搭配自身興趣、資源與實際經驗判斷。

        使用者描述：
        {user_input}
    """

    # 呼叫 Gemini API
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
        "歡迎使用 Gemini 職涯導向輔導 Bot。\n\n"
        "你可以輸入：\n"
        "/career 我是資工系學生，會 Python，但不知道未來要走 AI 還是後端\n\n"
        "我會根據你的描述，提供職涯方向、能力建議與 30 天行動計畫。\n\n"
        "可用指令：\n"
        "/help - 查看使用說明\n"
        "/flow - 查看機器人流程\n"
        "/career 你的職涯問題 - 取得職涯建議"
    )


# /help 使用說明
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "Gemini 職涯導向輔導 Bot 使用說明：\n\n"
        "/start - 開始使用 Bot\n"
        "/help - 查看使用說明\n"
        "/flow - 查看機器人流程\n"
        "/career 你的職涯問題 - 取得職涯建議\n\n"
        "使用範例：\n"
        "/career 我是大學生，會 Python，想走 AI 工程師，但不知道怎麼準備\n\n"
        "/career 我想轉職資料分析師，目前只會 Excel 和一點 Python\n\n"
        "/career 我喜歡設計，也會一點前端，適合走 UIUX 還是前端工程師？\n\n"
        "提醒：\n"
        "這個 Bot 提供的是職涯參考建議，不是絕對答案。"
    )


# /flow 流程說明
async def flow(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "Gemini 職涯輔導 Bot 流程說明：\n\n"
        "Step 1：使用者輸入職涯問題\n"
        "例如：/career 我是資工系學生，會 Python，不知道要走 AI 還是後端\n\n"

        "Step 2：Bot 取得使用者輸入內容\n"
        "程式會從 context.args 取得 /career 後面的文字。\n\n"

        "Step 3：程式組合 Prompt\n"
        "Bot 會把使用者問題整理成適合 Gemini 回答的提示詞。\n\n"

        "Step 4：呼叫 Gemini API\n"
        "程式會將 Prompt 傳送給 Gemini 模型。\n\n"

        "Step 5：Gemini 回傳分析結果\n"
        "內容包含職涯方向、能力建議與短期規劃。\n\n"

        "Step 6：Bot 將結果回覆給使用者\n"
        "使用者可以依照建議調整學習與職涯方向。"
    )


# /career 職涯輔導
async def career(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # 檢查是否輸入問題
    if not context.args:
        await update.message.reply_text(
            "用法：/career 你的職涯問題\n\n"
            "例如：\n"
            "/career 我是資工系學生，會 Python，不知道要走 AI 還是後端"
        )
        return

    user_input = " ".join(context.args) # 組合使用者問題

    await update.message.reply_text(
        "我正在根據你的描述產生職涯建議，請稍候。"
    )

    # 呼叫 Gemini API
    try:
        advice = ask_gemini_career_advice(user_input)

    except Exception as e:
        await update.message.reply_text(
            "呼叫 Gemini API 時發生錯誤，請稍後再試。\n\n"
            f"錯誤訊息：{e}"
        )
        return

    await update.message.reply_text(advice)


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
    app.add_handler(CommandHandler("flow", flow))
    app.add_handler(CommandHandler("career", career))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()