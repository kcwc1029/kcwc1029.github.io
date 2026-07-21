import smtplib

mySMTP = smtplib.SMTP('smtp.gmail.com', 587) # 建立一個 SMTP 物件
print(type(mySMTP)) # <class 'smtplib.SMTP'>