# 匯入 Telegram Bot 更新物件
from telegram import Update

# 匯入 Telegram Bot 功能模組
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# 匯入讀取 .env 工具
from dotenv import load_dotenv

# 匯入作業系統模組
import os


# 載入 .env 內容
load_dotenv()

# 取得 Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")


# /start 開始功能
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    顯示 Bot 介紹
    """

    await update.message.reply_text(
        "您好，歡迎使用電商 FAQ 自動回覆 Bot。\n\n"
        "我可以協助您查詢常見購物問題，例如：\n"
        "出貨、物流、退貨、退款、優惠、付款、發票、客服。\n\n"
        "您可以輸入 /flow 查看使用流程，\n"
        "或輸入 /faq 查看可查詢的 FAQ 主題。"
    )


# /help 指令說明
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    顯示所有指令
    """

    await update.message.reply_text(
        "電商 FAQ Bot 指令說明\n\n"
        "/start - 開始使用 Bot\n"
        "/help - 查看所有指令說明\n"
        "/flow - 查看機器人使用流程\n"
        "/faq - 查看可查詢的 FAQ 主題\n\n"
        "除了輸入指令之外，您也可以直接輸入問題。\n"
        "例如：\n"
        "我的商品什麼時候出貨？\n"
        "可以退貨嗎？\n"
        "支援信用卡付款嗎？\n"
        "有沒有優惠券？"
    )


# /flow 流程說明
async def flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    顯示 Bot 使用流程
    """

    await update.message.reply_text(
        "電商 FAQ 自動回覆 Bot 使用流程\n\n"
        "Step 1：使用者輸入問題\n"
        "例如：我想知道商品什麼時候出貨？\n\n"
        "Step 2：Bot 讀取使用者輸入的文字\n"
        "Bot 會取得你輸入的句子，並分析裡面是否有關鍵字。\n\n"
        "Step 3：Bot 判斷問題類型\n"
        "例如偵測到「出貨」，就會判斷這是出貨問題。\n\n"
        "Step 4：Bot 回覆對應 FAQ 答案\n"
        "系統會根據問題類型，回覆事先設計好的客服說明。\n\n"
        "Step 5：如果找不到關鍵字\n"
        "Bot 會提醒目前支援的 FAQ 主題，讓使用者知道可以問什麼。\n\n"
        "你可以直接輸入：出貨、物流、退貨、退款、優惠、付款、發票、客服。"
    )


# /faq FAQ 清單
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    顯示 FAQ 主題
    """

    await update.message.reply_text(
        "目前支援的 FAQ 主題如下：\n\n"
        "1. 出貨問題\n"
        "可輸入：出貨、寄出、什麼時候寄\n\n"
        "2. 物流配送\n"
        "可輸入：物流、配送、貨運、超商取貨\n\n"
        "3. 退貨退款\n"
        "可輸入：退貨、退款、換貨\n\n"
        "4. 優惠活動\n"
        "可輸入：優惠、折扣、折價券、優惠券\n\n"
        "5. 付款方式\n"
        "可輸入：付款、刷卡、信用卡、貨到付款\n\n"
        "6. 發票問題\n"
        "可輸入：發票、統編、電子發票\n\n"
        "7. 客服聯絡\n"
        "可輸入：客服、聯絡、人工客服"
    )


# FAQ 自動回覆功能
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    根據關鍵字回覆 FAQ
    """

    # 取得使用者輸入文字
    text = update.message.text.strip()

    # 出貨問題
    if "出貨" in text or "寄出" in text or "什麼時候寄" in text:
        reply = (
            "出貨說明：\n\n"
            "一般商品會在付款完成後 1～2 個工作天內出貨。\n"
            "若遇到週末、國定假日或大型促銷活動，出貨時間可能會稍微延後。\n\n"
            "如果您已完成付款，但超過 3 個工作天仍未出貨，建議聯絡客服協助查詢。"
        )

    # 物流配送問題
    elif "物流" in text or "配送" in text or "貨運" in text or "超商取貨" in text:
        reply = (
            "物流配送說明：\n\n"
            "目前支援以下配送方式：\n"
            "1. 宅配到府\n"
            "2. 超商取貨\n"
            "3. 貨運配送\n\n"
            "商品出貨後，系統會提供物流追蹤資訊，您可以依照物流編號查詢配送進度。"
        )

    # 退貨退款問題
    elif "退貨" in text or "退款" in text or "換貨" in text:
        reply = (
            "退貨退款說明：\n\n"
            "若商品有瑕疵、寄錯商品，或與訂單內容不符，可以申請退貨或退款。\n\n"
            "請注意：\n"
            "1. 請於收到商品後 7 天內提出申請。\n"
            "2. 商品需保持完整包裝。\n"
            "3. 若商品已拆封或使用，可能會影響退貨資格。\n\n"
            "若需要人工協助，請輸入「客服」。"
        )

    # 優惠活動問題
    elif "優惠" in text or "折扣" in text or "折價券" in text or "優惠券" in text:
        reply = (
            "優惠活動說明：\n\n"
            "目前常見優惠包含：\n"
            "1. 新會員註冊折扣\n"
            "2. 滿額免運活動\n"
            "3. 限時折價券\n"
            "4. 節慶促銷活動\n\n"
            "實際優惠內容會依活動時間調整，請以商城活動頁面公告為準。"
        )

    # 付款問題
    elif "付款" in text or "刷卡" in text or "信用卡" in text or "貨到付款" in text:
        reply = (
            "付款方式說明：\n\n"
            "目前支援以下付款方式：\n"
            "1. 信用卡付款\n"
            "2. ATM 轉帳\n"
            "3. 超商付款\n"
            "4. 貨到付款\n\n"
            "付款完成後，訂單狀態會自動更新。"
        )

    # 發票問題
    elif "發票" in text or "統編" in text or "電子發票" in text:
        reply = (
            "發票說明：\n\n"
            "本商城支援電子發票。\n"
            "如果需要公司報帳，可以在結帳時填寫統一編號。\n\n"
            "若訂單已成立但需要修改發票資訊，請盡快聯絡客服協助處理。"
        )

    # 客服問題
    elif "客服" in text or "聯絡" in text or "人工客服" in text:
        reply = (
            "客服聯絡方式：\n\n"
            "您可以透過以下方式聯絡客服：\n"
            "1. 官方網站客服中心\n"
            "2. Email：service@example.com\n"
            "3. 客服時間：週一至週五 09:00～18:00\n\n"
            "若遇到訂單、付款或退貨問題，建議提供訂單編號，客服會更快協助您查詢。"
        )

    # 找不到關鍵字
    else:
        reply = (
            "您好，我目前還無法判斷您的問題類型。\n\n"
            "您可以改用以下關鍵字詢問：\n"
            "出貨、物流、退貨、退款、優惠、付款、發票、客服\n\n"
            "也可以輸入 /faq 查看完整 FAQ 主題。"
        )

    # 回覆訊息
    await update.message.reply_text(reply)


# 主程式
def main() -> None:
    """
    建立並啟動 Bot
    """
    print("機器人啟用中")
    print("可以先輸出/help指令")
    

    # 建立 Bot 應用程式
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 加入指令處理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("flow", flow))
    app.add_handler(CommandHandler("faq", faq))

    # 加入文字訊息處理器
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    # 啟動 Bot
    app.run_polling()


# 程式進入點
if __name__ == "__main__":
    main()