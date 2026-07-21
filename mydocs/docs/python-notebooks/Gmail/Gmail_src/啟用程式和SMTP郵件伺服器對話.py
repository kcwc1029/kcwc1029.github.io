import smtplib

mySMTP = smtplib.SMTP('smtp.gmail.com', 587) # 建立一個 SMTP 物件

### 啟動伺服器 & 加密傳輸 
ehlo_response = mySMTP.ehlo() # 啟動與 SMTP 伺服器的對話 (mySMTP.ehlo()回傳職必須要是250，才算成功)
print("EHLO 回傳:", ehlo_response)
starttls_response = mySMTP.starttls() # 建立加密傳輸 (必須要回傳220，才算成功)
print("STARTTLS 回傳:", starttls_response)