import os
from pathlib import Path
from dotenv import load_dotenv
import smtplib
import requests
import yfinance as yf

from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header


### 環境變數
current_file = Path(__file__).resolve()  # 取得目前這個 Python 檔案的絕對路徑
project_root = current_file.parent.parent  # 往上返回兩層，取得專案根目錄
env_path = project_root / ".env"  # 指定 .env 檔案路徑

load_dotenv(dotenv_path=env_path)  # 載入 .env 環境變數


### 讀取環境變數
FromAddress = os.getenv("FromAddress")  # 寄件者 Email
AppPassword = os.getenv("AppPassword")  # Gmail 應用程式密碼


### 檢查環境變數
if not FromAddress or not AppPassword:
    print("錯誤：請確認 .env 裡面有 FromAddress 與 AppPassword")
    raise SystemExit


### 清理數字格式
def clean_number(value):
    return float(value.replace(",", "").replace("--", "0"))  # 移除逗號與缺值符號後轉成 float


### 取得台股資料
def get_tw_stock_data(stock_code):
    today = datetime.today()  # 取得今天日期
    date_text = today.strftime("%Y%m%d")  # 轉成 TWSE API 需要的日期格式

    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"  # 台灣證交所每日成交資訊 API

    params = {
        "response": "json",
        "date": date_text,
        "stockNo": stock_code
    }

    response = requests.get(url, params=params)  # 向台灣證交所送出查詢請求
    result = response.json()  # 將回傳內容轉成 JSON 格式

    if "data" not in result or len(result["data"]) < 2:
        return None  # 若資料不足，回傳 None

    data = result["data"]  # 取得每日交易資料

    latest = data[-1]  # 最新一筆交易資料
    previous = data[-2]  # 前一個交易日資料

    latest_date = latest[0]  # 最新交易日期
    volume = clean_number(latest[1])  # 成交股數
    open_price = clean_number(latest[3])  # 開盤價
    high_price = clean_number(latest[4])  # 最高價
    low_price = clean_number(latest[5])  # 最低價
    close_price = clean_number(latest[6])  # 收盤價

    previous_close = clean_number(previous[6])  # 前一個交易日收盤價

    return {
        "ticker": stock_code,
        "latest_date": latest_date,
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
        "volume": volume,
        "previous_close": previous_close
    }


### 取得美股資料
def get_us_stock_data(ticker_symbol):
    try:
        data = yf.download(
            ticker_symbol,
            period="10d",
            interval="1d",
            progress=False,
            auto_adjust=False,
            threads=False
        )  # 使用 yfinance 下載近 10 天每日交易資料

    except Exception as error:
        print("錯誤：yfinance 抓取失敗")
        print(error)
        return None

    # yfinance 有時會回傳多層欄位，這裡統一轉成單層欄位
    if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()  # 移除空值資料

    if len(data) < 2:
        return None  # 若資料不足，回傳 None

    latest = data.iloc[-1]  # 最新一筆交易資料
    previous = data.iloc[-2]  # 前一個交易日資料

    return {
        "ticker": ticker_symbol,
        "latest_date": data.index[-1].strftime("%Y-%m-%d"),
        "open": float(latest["Open"]),
        "high": float(latest["High"]),
        "low": float(latest["Low"]),
        "close": float(latest["Close"]),
        "volume": float(latest["Volume"]),
        "previous_close": float(previous["Close"])
    }


### 使用者輸入
to_address = input("請輸入收件人 Email：").strip()  # 輸入收件者 Email
ticker_symbol = input("請輸入股票或 ETF 代號，例如 2330、006208、0050、NVDA、AAPL：").strip()  # 輸入股票代號


### 檢查使用者輸入
if not to_address:
    print("錯誤：收件人 Email 不可以空白")
    raise SystemExit

if not ticker_symbol:
    print("錯誤：股票或 ETF 代號不可以空白")
    raise SystemExit


### 判斷台股或美股
if ticker_symbol.isdigit():
    stock_data = get_tw_stock_data(ticker_symbol)  # 純數字代號視為台股
else:
    stock_data = get_us_stock_data(ticker_symbol)  # 非純數字代號視為美股


### 檢查股票資料
if stock_data is None:
    print(f"錯誤：查無 {ticker_symbol} 的資料，請確認股票或 ETF 代號是否正確")
    raise SystemExit


### 取出股票資料
latest_date = stock_data["latest_date"]  # 最新交易日期
open_price = stock_data["open"]  # 開盤價
high_price = stock_data["high"]  # 最高價
low_price = stock_data["low"]  # 最低價
close_price = stock_data["close"]  # 收盤價
volume = stock_data["volume"]  # 成交量
previous_close = stock_data["previous_close"]  # 前一個交易日收盤價

change_amount = close_price - previous_close  # 計算漲跌金額
change_percent = (change_amount / previous_close) * 100  # 計算漲跌幅百分比


### 簡單解讀
if change_amount > 0:
    market_comment = "今日收盤價高於前一個交易日，短線表現偏強。"

elif change_amount < 0:
    market_comment = "今日收盤價低於前一個交易日，短線表現偏弱。"

else:
    market_comment = "今日收盤價與前一個交易日相同，股價變動不大。"


if close_price > open_price:
    intraday_comment = "盤中走勢來看，收盤價高於開盤價，代表買盤相對積極。"

elif close_price < open_price:
    intraday_comment = "盤中走勢來看，收盤價低於開盤價，代表賣壓相對明顯。"

else:
    intraday_comment = "盤中走勢來看，開盤價與收盤價相同，整體波動有限。"


### 組合信件
subject = f"【財經觀察報告】{ticker_symbol}"  # 郵件主旨

body = f"""
您好：

以下是您查詢的股票 / ETF 財經觀察報告。

股票或 ETF 代號：{ticker_symbol}
最新交易日期：{latest_date}

開盤價：{open_price:.2f}
最高價：{high_price:.2f}
最低價：{low_price:.2f}
最新收盤價：{close_price:.2f}
成交量：{volume:,.0f}

與前一個交易日相比：
漲跌金額：{change_amount:.2f}
漲跌幅：{change_percent:.2f}%

簡單解讀：
{market_comment}
{intraday_comment}

提醒：
本信件僅供教學練習，不構成投資建議。
"""


### 建立郵件內容
msg = MIMEText(body, "plain", "utf-8")  # 建立純文字郵件內容
msg["Subject"] = Header(subject, "utf-8")  # 設定郵件主旨
msg["From"] = FromAddress  # 設定寄件者
msg["To"] = to_address  # 設定收件者


### 寄送郵件
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.ehlo()  # 啟動與 SMTP 伺服器的對話
        server.starttls()  # 建立 TLS 加密連線
        server.login(FromAddress, AppPassword)  # 登入 Gmail SMTP 伺服器

        server.sendmail(
            FromAddress,
            [to_address],
            msg.as_string()
        )  # 寄送財經報告郵件

except Exception as error:
    print("錯誤：Gmail 寄送失敗")
    print(error)
    raise SystemExit


print(f"財經報告已寄出至：{to_address}")