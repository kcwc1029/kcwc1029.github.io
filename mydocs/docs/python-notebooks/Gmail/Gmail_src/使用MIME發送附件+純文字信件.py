import os
from pathlib import Path
from dotenv import load_dotenv
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header


### 環境變數
current_file = Path(__file__).resolve()  # 取得目前執行檔的絕對路徑
project_root = current_file.parent.parent  # 往上返回兩層，回到專案根目錄
env_path = project_root / ".env"  # 組合 .env 檔案路徑

load_dotenv(dotenv_path=env_path)  # 載入指定位置的環境變數


### 讀取環境變數
AppPassword = os.getenv("AppPassword")  # Gmail App Password
FromAddress = os.getenv("FromAddress")  # 寄件者信箱
ToAddress = os.getenv("ToAddress")  # 收件者信箱


### 郵件設定
subject = "【課程即將上課通知】"  # 郵件主旨

text_content = """
您好：

附件為本次課程講義 PDF，
請記得提前下載與閱讀。

謝謝。
"""


### PDF 路徑
# 指向欲附加的 PDF 檔案
pdf_path = project_root / "Gmail_datasets" / "產業新尖兵計畫-1120701.pdf"


### 建立郵件主體
# 使用 MIMEMultipart 才能同時包含：
# 1. 郵件本文
# 2. 附件檔案
msg = MIMEMultipart()

msg["Subject"] = Header(subject, "utf-8")
msg["From"] = FromAddress
msg["To"] = ToAddress


### 加入純文字內容
# MIMEText 用來建立郵件本文
msg.attach(
    MIMEText(
        text_content,
        "plain",
        "utf-8"
    )
)


### 加入 PDF 附件
# 以二進位模式讀取 PDF 檔案
with open(pdf_path, "rb") as file:

    pdf_file = MIMEApplication(file.read())

    # 設定附件資訊
    # filename 使用 UTF-8，避免中文檔名亂碼
    pdf_file.add_header(
        "Content-Disposition",
        "attachment",
        filename=("utf-8", "", pdf_path.name)
    )

    msg.attach(pdf_file)


### 準備收件人清單
# sendmail() 第二個參數必須是 Email List
all_recipients = [ToAddress]


### 登入 SMTP 並寄送郵件
with smtplib.SMTP("smtp.gmail.com", 587) as server:

    server.ehlo()  # 啟動 SMTP 連線

    server.starttls()  # 升級為 TLS 加密傳輸

    server.login(
        FromAddress,
        AppPassword
    )  # 登入 Gmail

    server.sendmail(
        FromAddress,
        all_recipients,
        msg.as_string()
    )  # 寄送郵件


print("郵件已寄出！")