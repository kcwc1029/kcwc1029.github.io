import os
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.header import Header

### 環境變數
current_file = Path(__file__).resolve() # 取得目前這個 main.py 檔案的絕對路徑
project_root = current_file.parent.parent # 透過 .parent 往上跳兩層，回到專案根目錄 (my_project/)
env_path = project_root / ".env" # 指定根目錄底下的 .env 檔案路徑
load_dotenv(dotenv_path=env_path) # 載入指定路徑的 .env 檔案


### 讀取環境變數
AppPassword = os.getenv("AppPassword")
LoginEmail = os.getenv("LoginEmail")
FromAddress = os.getenv("FromAddress")
ToAddress = os.getenv("ToAddress")

### 設定郵件標題、寄件者、收件者
subject = '【課程即將上課通知】'
cc_user = ""
bcc_user = ""
msg = """
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

### 建立郵件內容
msg = MIMEText(msg, 'plain', 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')
msg['From'] = Header(f"<{FromAddress}>", 'utf-8') # 寄件人名稱也可以用中文
msg['To'] = ToAddress
msg['Cc'] = cc_user


### 準備收件人清單 (Bcc 在這裡加入)
# sendmail 需要一個「真正要寄送的 Email 地址列表」
# Bcc 的人要加在這裡，但不要加在 msg['Bcc'] (因為 Bcc 就是要隱藏)
all_recipients = [ToAddress, cc_user, bcc_user]


### 登入並寄送郵件
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.ehlo()  # 啟動與 SMTP 伺服器的對話
    server.starttls()  # 建立加密傳輸
    server.login(FromAddress, AppPassword)  # 登入
    server.sendmail(FromAddress, all_recipients, msg.as_string())  # 寄送郵件

print("郵件已寄出！")