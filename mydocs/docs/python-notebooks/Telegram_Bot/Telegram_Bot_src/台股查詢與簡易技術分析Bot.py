# 安裝套件：
# uv add yfinance
# uv add pandas

from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv

import yfinance as yf
import pandas as pd
import os


load_dotenv() # 載入 .env 檔案
BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token

API_BASE_URL = "https://api.frankfurter.dev"


# 計算 RSI 技術指標
def calculate_rsi(
    prices: pd.Series,
    period: int = 14
) -> float:

    delta = prices.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return float(rsi.iloc[-1])


# 轉換台股代碼格式
def format_tw_stock_symbol(code: str) -> str:
    code = code.upper().strip()

    # 已包含市場代碼時直接回傳
    if "." in code:
        return code

    return f"{code}.TW" # 預設上市股票


# 分析股票資料
def analyze_stock(symbol: str) -> dict | None:

    stock = yf.Ticker(symbol)

    # 抓取最近 6 個月資料
    df = stock.history(period="6mo")

    # 查無資料時回傳 None
    if df.empty:
        return None

    # 計算均線
    df["MA5"] = df["Close"].rolling(window=5).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA60"] = df["Close"].rolling(window=60).mean()

    latest = df.iloc[-1] # 最新資料
    previous = df.iloc[-2] # 前一天資料

    close_price = float(latest["Close"])
    previous_close = float(previous["Close"])

    change = close_price - previous_close
    change_percent = change / previous_close * 100

    ma5 = float(latest["MA5"])
    ma20 = float(latest["MA20"])
    ma60 = float(latest["MA60"])

    rsi = calculate_rsi(df["Close"])

    volume = int(latest["Volume"])

    avg_volume_20 = int(
        df["Volume"].rolling(window=20).mean().iloc[-1]
    )

    score = 0
    reasons = []

    # 股價站上 MA20
    if close_price > ma20:
        score += 1
        reasons.append("股價站上 20 日均線，短線走勢偏強。")

    else:
        reasons.append("股價低於 20 日均線，短線走勢偏弱。")

    # MA20 高於 MA60
    if ma20 > ma60:
        score += 1
        reasons.append("20 日均線高於 60 日均線，中期趨勢偏多。")

    else:
        reasons.append("20 日均線低於 60 日均線，中期趨勢尚未轉強。")

    # RSI 合理區間
    if 40 <= rsi <= 70:
        score += 1
        reasons.append("RSI 位於合理區間，尚未明顯過熱。")

    elif rsi > 70:
        reasons.append("RSI 高於 70，短線可能偏熱。")

    else:
        reasons.append("RSI 低於 40，買盤力道可能較弱。")

    # 成交量放大
    if volume > avg_volume_20:
        score += 1
        reasons.append("成交量高於 20 日均量，市場關注度增加。")

    else:
        reasons.append("成交量低於 20 日均量，市場動能較普通。")

    # 避免追高
    if close_price < ma20 * 1.10:
        score += 1
        reasons.append("股價沒有明顯遠離 20 日均線，追高風險較低。")

    else:
        reasons.append("股價已明顯高於 20 日均線，可能有追高風險。")

    # 根據分數給出建議
    if score >= 4:
        suggestion = (
            "偏多觀察，可以列入關注，但仍需搭配基本面與風險控管。"
        )

    elif score >= 2:
        suggestion = (
            "中性觀察，訊號尚未完全明確，不建議急著追高。"
        )

    else:
        suggestion = (
            "偏弱觀察，目前技術面條件不足，建議保守看待。"
        )

    return {
        "symbol": symbol,
        "close_price": close_price,
        "change": change,
        "change_percent": change_percent,
        "ma5": ma5,
        "ma20": ma20,
        "ma60": ma60,
        "rsi": rsi,
        "volume": volume,
        "avg_volume_20": avg_volume_20,
        "score": score,
        "suggestion": suggestion,
        "reasons": reasons,
    }


# /start 開始使用
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "歡迎使用台股查詢與簡易分析 Bot。\n\n"
        "你可以輸入：\n"
        "/stock 2330\n"
        "/stock 0050\n"
        "/stock 2317\n\n"
        "如果不知道怎麼使用，可以輸入：\n"
        "/help"
    )


# /help 使用說明
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "台股查詢 Bot 使用說明：\n\n"
        "/start - 開始使用\n"
        "/help - 查看使用說明\n"
        "/flow - 查看機器人流程\n"
        "/stock 股票代碼 - 查詢台股資訊\n\n"
        "範例：\n"
        "/stock 2330\n"
        "/stock 0050\n"
        "/stock 2317\n\n"
        "系統會回傳：\n"
        "1. 最新收盤價\n"
        "2. 漲跌幅\n"
        "3. 5 日、20 日、60 日均線\n"
        "4. RSI 指標\n"
        "5. 成交量\n"
        "6. 簡易買進評估\n\n"
        "提醒：本 Bot 僅供教學與參考，不構成投資建議。"
    )


# /flow 流程說明
async def flow(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "台股查詢 Bot 流程說明：\n\n"
        "Step 1：使用者輸入股票代碼\n"
        "例如：/stock 2330\n\n"

        "Step 2：程式轉換股票代碼\n"
        "例如：2330 會轉成 2330.TW\n\n"

        "Step 3：Bot 透過 yfinance 抓取最近 6 個月資料\n\n"

        "Step 4：程式計算技術指標\n"
        "包含 MA5、MA20、MA60、RSI、成交量等。\n\n"

        "Step 5：程式根據簡易規則評分\n"
        "例如是否站上均線、RSI 是否過熱、成交量是否放大。\n\n"

        "Step 6：Bot 回覆股票資訊與觀察建議\n\n"

        "提醒：這是教學用分析，不代表投資建議。"
    )


# /stock 查詢股票
async def stock_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # 檢查是否輸入股票代碼
    if not context.args:
        await update.message.reply_text(
            "用法：/stock 股票代碼\n"
            "例如：/stock 2330"
        )
        return

    stock_code = context.args[0]

    symbol = format_tw_stock_symbol(stock_code)

    await update.message.reply_text(
        f"正在查詢 {symbol}，請稍候..."
    )

    # 查詢股票資料
    try:
        result = analyze_stock(symbol)

    except Exception as e:
        await update.message.reply_text(
            "查詢股票資料時發生錯誤，請稍後再試。\n"
            f"錯誤訊息：{e}"
        )
        return

    # 查無資料
    if result is None:
        await update.message.reply_text(
            "查不到這個股票代碼，請確認是否輸入正確。\n"
            "例如：/stock 2330"
        )
        return

    reasons_text = "\n".join(
        [f"- {reason}" for reason in result["reasons"]]
    )

    reply = (
        f"股票代碼：{result['symbol']}\n\n"
        f"最新收盤價：{result['close_price']:.2f}\n"
        f"漲跌：{result['change']:.2f} "
        f"({result['change_percent']:.2f}%)\n\n"

        f"技術指標：\n"
        f"MA5：{result['ma5']:.2f}\n"
        f"MA20：{result['ma20']:.2f}\n"
        f"MA60：{result['ma60']:.2f}\n"
        f"RSI：{result['rsi']:.2f}\n\n"

        f"成交量：{result['volume']:,}\n"
        f"20 日均量：{result['avg_volume_20']:,}\n\n"

        f"簡易評分：{result['score']} / 5\n"
        f"觀察建議：{result['suggestion']}\n\n"

        f"分析原因：\n"
        f"{reasons_text}\n\n"

        f"提醒：本分析僅供教學與參考，不構成投資建議。"
    )

    await update.message.reply_text(reply)


# 主程式
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("flow", flow))
    app.add_handler(CommandHandler("stock", stock_command))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()