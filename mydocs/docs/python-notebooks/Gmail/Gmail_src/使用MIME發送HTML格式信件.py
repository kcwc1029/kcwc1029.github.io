import os
import smtplib
from pathlib import Path
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


### 環境變數
current_file = Path(__file__).resolve() # 取得目前檔案的絕對路徑
project_root = current_file.parent.parent # 回到專案根目錄
env_path = project_root / ".env" # 指定 .env 檔案路徑
load_dotenv(dotenv_path=env_path) # 載入環境變數


### 讀取環境變數
AppPassword = os.getenv("AppPassword")
LoginEmail = os.getenv("LoginEmail")
FromAddress = os.getenv("FromAddress")
ToAddress = os.getenv("ToAddress")


### 郵件基本設定
subject = "【課程即將上課通知】"
cc_user = ""
bcc_user = ""


### HTML 郵件內容
html_body = """
<div style="font-family:Arial, 'Microsoft JhengHei', sans-serif; color:#333333; line-height:1.8; font-size:16px;">
  <p>您好：</p>

  <p>
    向您說明與確認下週的行程安排，以下為下週的會議時間與我的請假規劃：
  </p>

  <p>
    <strong>下週三 ([日期])：</strong>預計參與 [會議A名稱]。
  </p>

  <p>
    <strong>下週四 ([日期])：</strong>預計參與 [會議B名稱]。
  </p>

  <p>
    <strong>下週五 ([日期])：</strong>因 [請假事由]，預計請假一天。
  </p>

  <p style="background-color:#fff7ed; border-left:4px solid #f97316; padding:12px 14px;">
    請假當天的業務工作我會提前處理完畢。若當天有緊急突發狀況，我仍會保持手機暢通，
    或您可以直接聯絡代理人 [代理人名字]，我已與他完成相關業務的交接。
  </p>

  <p>
    以上行程與請假申請，再請您撥冗核准，謝謝！
  </p>

  <p>
    祝 順心
  </p>
</div>
"""


### 建立郵件物件
msg = MIMEText(html_body, "html", "utf-8")


### 設定郵件標頭
msg["Subject"] = Header(subject, "utf-8")
msg["From"] = formataddr(("課程通知", FromAddress)) # 顯示寄件人名稱
msg["To"] = ToAddress


### 準備收件人清單
# sendmail() 需要實際寄送的 Email 清單
all_recipients = [ToAddress]


### 加入副本收件人
if cc_user:
    msg["Cc"] = cc_user
    all_recipients.append(cc_user)


### 加入密件副本收件人
# Bcc 不寫入郵件標頭，避免被其他收件人看到
if bcc_user:
    all_recipients.append(bcc_user)


### 連線 Gmail SMTP 並寄送郵件
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo() # 啟動 SMTP 對話
    server.starttls() # 建立 TLS 加密連線
    server.login(LoginEmail, AppPassword) # 登入 Gmail
    server.sendmail(
        FromAddress,
        all_recipients,
        msg.as_string()
    ) # 寄送郵件


print("郵件已寄出！")