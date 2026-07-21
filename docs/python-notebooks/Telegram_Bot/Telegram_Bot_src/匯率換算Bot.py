from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv

import os
import requests


load_dotenv() # 載入 .env 檔案
BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token

API_BASE_URL = "https://api.frankfurter.dev" # 匯率 API 網址


# 查詢指定幣別兌換台幣匯率
def fetch_rate_to_twd(currency: str) -> float | None:

    response = requests.get(
        f"{API_BASE_URL}/v2/rate/{currency.upper()}/TWD",
        timeout=10
    )

    response.raise_for_status() # HTTP 錯誤時拋出例外

    data = response.json() # 解析 JSON

    return data.get("rate")


# /start 開始使用
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    text = (
        "您好，我是台幣匯率換算機器人。\n\n"
        "你可以輸入：\n"
        "/convert USD 100\n"
        "/convert JPY 5000\n"
        "/convert EUR 50\n\n"
        "我會幫你換算成台幣 TWD。\n\n"
        "如果不知道怎麼使用，可以輸入：\n"
        "/help"
    )

    await update.message.reply_text(text)


# /help 使用說明
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    text = (
        "【機器人使用流程】\n\n"
        "1. 輸入指令\n"
        "格式為：\n"
        "/convert 幣別 數值\n\n"

        "2. 範例\n"
        "/convert USD 100\n"
        "代表將 100 美元換算成台幣。\n\n"

        "/convert JPY 5000\n"
        "代表將 5000 日圓換算成台幣。\n\n"

        "/convert EUR 50\n"
        "代表將 50 歐元換算成台幣。\n\n"

        "3. 常見幣別代碼\n"
        "USD：美元\n"
        "EUR：歐元\n"
        "JPY：日圓\n"
        "KRW：韓元\n"
        "GBP：英鎊\n"
        "AUD：澳幣\n"
        "CAD：加幣\n\n"

        "4. 注意事項\n"
        "目前所有幣別都會換算成 TWD 台幣。\n"
        "請使用格式：/convert 幣別 數值"
    )

    await update.message.reply_text(text)


# /convert 幣別換算
async def convert(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # 檢查參數數量
    if len(context.args) != 2:
        await update.message.reply_text(
            "格式錯誤，請輸入：/convert 幣別 數值\n"
            "例如：/convert USD 100"
        )
        return

    currency = context.args[0].upper() # 取得幣別代碼

    # 驗證金額格式
    try:
        amount = float(context.args[1])

    except ValueError:
        await update.message.reply_text(
            "金額格式錯誤，請輸入數字，例如：/convert USD 100"
        )
        return

    # 檢查金額是否大於 0
    if amount <= 0:
        await update.message.reply_text(
            "金額必須大於 0。"
        )
        return

    # 查詢匯率
    try:
        rate_value = fetch_rate_to_twd(currency)

    except requests.RequestException:
        await update.message.reply_text(
            "查詢匯率時發生錯誤，請稍後再試。"
        )
        return

    # 找不到幣別
    if rate_value is None:
        await update.message.reply_text(
            "找不到這個幣別，請確認代碼是否正確。"
        )
        return

    twd_amount = amount * rate_value # 計算台幣金額

    await update.message.reply_text(
        f"{amount:.2f} {currency} = {twd_amount:.2f} TWD\n"
        f"匯率：1 {currency} = {rate_value:.4f} TWD"
    )


# 主程式
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("convert", convert))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()