import os
from pathlib import Path
from dotenv import load_dotenv
import smtplib
import csv
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header


### 環境變數
current_file = Path(__file__).resolve()  # 取得目前這個 Python 檔案的絕對路徑
project_root = current_file.parent.parent  # 往上返回兩層，取得專案根目錄
env_path = project_root / ".env"  # 指定 .env 檔案路徑

load_dotenv(dotenv_path=env_path)  # 載入 .env 環境變數


### 讀取環境變數
AppPassword = os.getenv("AppPassword")  # Gmail 應用程式密碼
FromAddress = os.getenv("FromAddress")  # 寄件者 Email


### 寄件人名稱
senderName = "專屬行銷團隊"  # 顯示在收件者信箱中的寄件人名稱


### CSV 路徑
csv_path = project_root / "Gmail_datasets" / "customers.csv"  # 客戶資料 CSV 檔案路徑


### PDF 路徑
pdf_path = project_root / "Gmail_datasets" / "產業新尖兵計畫-1120701.pdf"  # 附件 PDF 檔案路徑


### 建立與 SMTP 伺服器的連線
with smtplib.SMTP("smtp.gmail.com", 587) as server:

    server.ehlo()  # 啟動與 SMTP 伺服器的對話
    server.starttls()  # 建立 TLS 加密連線

    server.login(FromAddress, AppPassword)  # 登入 Gmail SMTP 伺服器

    ### 開啟並讀取 CSV 檔案
    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)  # 將 CSV 每一列轉成 dict，方便用欄位名稱取值

        for row in reader:

            customer_name = row["姓名"]  # 讀取客戶姓名
            gender = row["性別"]  # 讀取性別欄位
            customer_email = row["信箱"]  # 讀取客戶 Email
            product = row["購買商品"]  # 讀取購買商品名稱

            ### 自動判斷稱謂
            title = "先生" if gender.upper() == "M" else "小姐"

            ### 客製化信件
            subject = f"【專屬通知】感謝您購買 {product}"  # 根據商品名稱產生信件主旨

            text_content = f"""親愛的 {customer_name} {title} 您好：

感謝您近期選購我們的【{product}】。

附件為本次課程講義 PDF，
請記得提前下載與閱讀。

祝您順心
{senderName} 敬上
"""

            ### 建立郵件
            msg = MIMEMultipart()  # 建立可包含文字與附件的郵件物件

            msg["Subject"] = Header(subject, "utf-8")  # 設定郵件主旨
            msg["From"] = Header(f"{senderName} <{FromAddress}>", "utf-8")  # 設定寄件人
            msg["To"] = customer_email  # 設定收件人

            ### 加入純文字內容
            msg.attach(MIMEText(text_content, "plain", "utf-8"))  # 加入純文字信件內容

            ### 加入 PDF 附件
            with open(pdf_path, "rb") as pdf_file:

                attachment = MIMEApplication(pdf_file.read())  # 讀取 PDF 並建立附件物件

                attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=("utf-8", "", pdf_path.name)
                )  # 設定附件檔名，避免中文檔名亂碼

                msg.attach(attachment)  # 將 PDF 附件加入郵件

            ### 寄送郵件
            server.sendmail(
                FromAddress,
                [customer_email],
                msg.as_string()
            )  # 寄送客製化郵件給目前這位客戶

            print(f"已成功發送客製化信件至：{customer_name} ({customer_email})")

            time.sleep(1)  # 每寄一封信暫停 1 秒，避免短時間大量寄送


print("所有客製化信件發送完畢！")