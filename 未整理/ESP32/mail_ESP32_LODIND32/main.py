from machine import Pin, ADC
import utime
import umail
import connect_wifi
import config

connect_wifi.connect_wifi_led(ssid=config.WIFI_SSID, passwd=config.WIFI_PASSWORD, timeout=15)

sender_email = config.SEND_EMAIL # "<寄件者的Gmail電郵地址>"
sender_name = config.SEND_NAME
sender_app_password = config.EMAIL_APPLICATION_PASSWORD # "<應用程式密碼>"
recipient_email = config.RECIVE_EMAIL # "<收件者的電郵地址>"
email_subject = config.EMAIL_SUBJECT
email_content = config.EMAIL_CONTENT


print("送出Email!")
smtp = umail.SMTP("smtp.gmail.com", 587, use_ssl=False)
smtp.login(sender_email, sender_app_password)
smtp.to(recipient_email)
smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
smtp.write("Subject:" + email_subject + "\n")
smtp.write(email_content)
smtp.send()
smtp.quit()
utime.sleep(10)
