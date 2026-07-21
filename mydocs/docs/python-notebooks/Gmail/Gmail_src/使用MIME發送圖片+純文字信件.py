import os
from pathlib import Path
from dotenv import load_dotenv
import smtplib
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header


### 環境變數
current_file = Path(__file__).resolve() # 取得目前檔案的絕對路徑
project_root = current_file.parent.parent # 回到專案根目錄
env_path = project_root / ".env" # 指定 .env 檔案位置
load_dotenv(dotenv_path=env_path) # 載入 .env 環境變數


### 讀取環境變數
AppPassword = os.getenv("AppPassword")
FromAddress = os.getenv("FromAddress")
ToAddress = os.getenv("ToAddress")


### 郵件設定
subject = "【課程即將上課通知】"
text_content = """
雨是神明的煙花
我為誰在等啊
等到滿身濕透吧
也捨不得回家
我滾燙的願望
遇到你就蒸發
沒等到的回答
躲在雲裡暗啞
我的愛不值一提嗎
"""


### 圖片網址
image_url = "https://i.pinimg.com/736x/63/16/b2/6316b20446639cd7f923882cc0d5b0a5.jpg"


### 建立郵件物件
msg = MIMEMultipart()
msg["Subject"] = Header(subject, "utf-8")
msg["From"] = FromAddress
msg["To"] = ToAddress


### 加入文字內容
msg.attach(MIMEText(text_content, "plain", "utf-8"))


### 下載線上圖片
response = requests.get(image_url)
response.raise_for_status() # 如果圖片下載失敗，會直接拋出錯誤


### 建立圖片附件
image = MIMEImage(response.content)
image.add_header(
    "Content-Disposition",
    "attachment",
    filename="notice.jpg"
)


### 加入圖片附件
msg.attach(image)


### 準備收件人清單
all_recipients = [ToAddress]


### 登入並寄送郵件
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo() # 啟動 SMTP 對話
    server.starttls() # 建立 TLS 加密連線
    server.login(FromAddress, AppPassword) # 登入 Gmail
    server.sendmail(
        FromAddress,
        all_recipients,
        msg.as_string()
    ) # 寄送郵件


print("郵件已寄出！")