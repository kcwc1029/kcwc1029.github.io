import smtplib
import os
from pathlib import Path
from dotenv import load_dotenv

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


mySMTP = smtplib.SMTP('smtp.gmail.com', 587) # 建立一個 SMTP 物件
ehlo_response = mySMTP.ehlo() # 啟動與 SMTP 伺服器的對話 (mySMTP.ehlo()回傳職必須要是250，才算成功)
starttls_response = mySMTP.starttls() # 建立加密傳輸 (必須要回傳220，才算成功)
login_response = mySMTP.login(LoginEmail, AppPassword) # 登入 (必須要回傳235，才算成功)
print(login_response)


### 撰寫一封簡單gmail
status = mySMTP.sendmail(
    FromAddress, # 寄件者
    ToAddress, # 收件者
    # 信件內容 (標題與內文之間要空一行，而且只能用英文)
	"Subject: 2026.04.20 send gmail test.\n\nIt's very hot today."
) # 寄信 (status回傳{}表示成功)()只能用英文)

mySMTP.quit() # 結束與 SMTP 伺服器的對話 (必須要回傳221，才算成功)
print("信件發送成功")