from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from dotenv import load_dotenv
import os


load_dotenv() # 載入 .env 設定
BOT_TOKEN = os.getenv("BOT_TOKEN") # 取得 Bot Token


# 建立主選單鍵盤
def build_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        ["查詢訂單", "物流配送"],
        ["退貨退款", "優惠活動"],
        ["付款方式", "聯絡客服"],
        ["查看流程", "關閉選單"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True, # 自動調整鍵盤大小
        one_time_keyboard=False # 選單保持顯示
    )


# /start 開始使用
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用電商客服 Reply Keyboard Bot。\n\n"
        "你可以輸入 /menu 開啟主選單，\n"
        "或輸入 /flow 查看機器人流程。"
    )


# /menu 顯示主選單
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "請從下方主選單選擇功能：",
        reply_markup=build_main_keyboard()
    )


# /help 顯示指令說明
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "指令說明：\n\n"
        "/start - 開始使用 Bot\n"
        "/menu - 開啟 Reply Keyboard 主選單\n"
        "/flow - 查看機器人流程\n"
        "/close - 關閉主選單\n\n"
        "你也可以直接點選下方選單按鈕：\n"
        "查詢訂單、物流配送、退貨退款、優惠活動、付款方式、聯絡客服。"
    )


# /flow 顯示 Bot 流程
async def flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "電商 Reply Keyboard Bot 流程說明：\n\n"
        "Step 1：使用者輸入 /menu\n"
        "Bot 會顯示一組常駐主選單。\n\n"
        "Step 2：使用者點選選單按鈕\n"
        "Reply Keyboard 的按鈕本質上會送出一段文字。\n"
        "例如點選「物流配送」，Bot 會收到文字：物流配送。\n\n"
        "Step 3：MessageHandler 接收文字\n"
        "程式會用 handle_text() 判斷使用者點了哪個選項。\n\n"
        "Step 4：根據文字內容回覆對應功能\n"
        "例如：物流配送、退貨退款、付款方式等。\n\n"
        "Step 5：若使用者輸入不支援的內容\n"
        "Bot 會提醒使用者點選主選單，或輸入 /menu 重新開啟。"
    )


# /close 關閉主選單
async def close_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "已關閉主選單。",
        reply_markup=ReplyKeyboardRemove()
    )


# 處理使用者點選的選單文字
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip() # 去除前後空白

    if text == "查詢訂單":
        reply = (
            "查詢訂單：\n\n"
            "你可以到會員中心查看訂單狀態。\n"
            "常見狀態包含：待付款、處理中、已出貨、已完成。"
        )

    elif text == "物流配送":
        reply = (
            "物流配送：\n\n"
            "目前支援宅配到府與超商取貨。\n"
            "商品出貨後，系統會提供物流追蹤編號。"
        )

    elif text == "退貨退款":
        reply = (
            "退貨退款：\n\n"
            "若商品有瑕疵或寄錯商品，收到商品後 7 天內可申請退貨。\n"
            "請保留商品完整包裝。"
        )

    elif text == "優惠活動":
        reply = (
            "優惠活動：\n\n"
            "目前有新會員折扣、滿額免運與限時折價券。"
        )

    elif text == "付款方式":
        reply = (
            "付款方式：\n\n"
            "支援信用卡、ATM 轉帳、超商付款與貨到付款。"
        )

    elif text == "聯絡客服":
        reply = (
            "聯絡客服：\n\n"
            "客服信箱：service@example.com\n"
            "客服時間：週一至週五 09:00～18:00"
        )

    elif text == "查看流程":
        await flow(update, context)
        return

    elif text == "關閉選單":
        await close_menu(update, context)
        return

    else:
        reply = (
            "目前沒有這個選項。\n\n"
            "請點選下方主選單，或輸入 /menu 開啟選單。"
        )

    await update.message.reply_text(reply) # 回覆對應內容


# 建立並啟動 Bot
def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/menu指令跳出選單")

    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot 應用程式
    app.add_handler(CommandHandler("start", start)) # /start 指令
    app.add_handler(CommandHandler("help", help_command)) # /help 指令
    app.add_handler(CommandHandler("menu", menu)) # /menu 指令
    app.add_handler(CommandHandler("flow", flow)) # /flow 指令
    app.add_handler(CommandHandler("close", close_menu)) # /close 指令

    # 處理 Reply Keyboard 送出的文字
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.run_polling() # 啟動輪詢


if __name__ == "__main__":
    main()