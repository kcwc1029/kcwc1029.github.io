```python
import smtplib

from pathlib import Path

from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import gradio as gr


### Email 工具
def split_emails(email_text):
    emails = []  # 建立空列表，用來存放整理後的 Email

    for email in email_text.split(","):  # 使用逗號分割多個收件人 Email
        email = email.strip()  # 移除 Email 前後空白

        if email:
            emails.append(email)  # 若 Email 不為空，加入列表

    return emails


### 附件處理
def attach_files(msg, files, is_image=False):

    if not files:
        return  # 若沒有上傳檔案，直接結束函式

    for file in files:

        file_path = Path(file.name)  # 取得上傳檔案路徑

        with open(file_path, "rb") as f:
            file_data = f.read()  # 以二進位模式讀取檔案內容

        if is_image:
            part = MIMEImage(file_data)  # 建立圖片附件物件

        else:
            part = MIMEBase(
                "application",
                "octet-stream"
            )  # 建立一般附件物件

            part.set_payload(file_data)  # 將檔案內容放入附件物件

            encoders.encode_base64(part)  # 將附件轉成 Base64，方便 Email 傳送

        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{file_path.name}"'
        )  # 設定附件檔名

        msg.attach(part)  # 將附件加入郵件


### 顯示密碼欄位
def unlock_password():

    return gr.update(
        visible=True,
        interactive=True
    )  # 顯示並啟用密碼輸入欄位


### 寄送 Email
def send_email(
    from_address,
    app_password,
    to_addresses_text,
    subject,
    body,
    image_files,
    attachment_files
):

    try:

        ### 檢查必填欄位
        if not from_address.strip():
            return "❌ 請輸入寄件人信箱"

        if not app_password.strip():
            return "❌ 請輸入 Gmail 應用程式密碼"

        if not to_addresses_text.strip():
            return "❌ 請輸入收件人信箱"

        if not subject.strip():
            return "❌ 請輸入信件標題"

        if not body.strip():
            return "❌ 請輸入信件內容"

        ### 整理收件人 Email
        to_addresses = split_emails(
            to_addresses_text
        )  # 將使用者輸入的多個 Email 轉成列表

        ### 建立郵件
        msg = MIMEMultipart()  # 建立可包含文字、圖片與附件的郵件物件

        msg["From"] = from_address  # 設定寄件人

        msg["To"] = ", ".join(
            to_addresses
        )  # 設定收件人顯示文字

        msg["Subject"] = subject  # 設定信件標題

        msg.attach(
            MIMEText(
                body,
                "plain",
                "utf-8"
            )
        )  # 加入純文字信件內容

        ### 加入圖片附件
        attach_files(
            msg,
            image_files,
            is_image=True
        )

        ### 加入一般附件
        attach_files(
            msg,
            attachment_files,
            is_image=False
        )

        ### 登入 Gmail SMTP 並寄送郵件
        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.ehlo()  # 啟動與 SMTP 伺服器的對話

            server.starttls()  # 建立 TLS 加密連線

            server.login(
                from_address,
                app_password
            )  # 登入 Gmail SMTP

            server.sendmail(
                from_address,
                to_addresses,
                msg.as_string()
            )  # 寄送郵件給所有收件人

        return (
            "✅ 郵件寄送成功\n\n"
            f"收件人數量：{len(to_addresses)}"
        )

    except Exception as error:

        return (
            "❌ 郵件寄送失敗\n\n"
            f"{error}"
        )


### Gradio UI
with gr.Blocks(
    title="系統訊息發送工具",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
# 📧 系統訊息發送工具

透過 Gmail SMTP 發送通知信件。
"""
    )

    ### 寄件設定
    with gr.Group():

        gr.Markdown(
            "## 寄件設定"
        )

        from_address = gr.Textbox(
            label="寄件人信箱",
            placeholder="example@gmail.com"
        )

        with gr.Row():

            unlock_btn = gr.Button(
                "🔓 解鎖密碼欄位",
                scale=1
            )

            app_password = gr.Textbox(
                label="Gmail 應用程式密碼",
                type="password",
                visible=False,
                interactive=False,
                scale=3
            )

    ### 收件設定
    with gr.Group():

        gr.Markdown(
            "## 收件設定"
        )

        to_addresses = gr.Textbox(
            label="收件人信箱",
            placeholder=(
                "student1@gmail.com,"
                "student2@gmail.com"
            )
        )

    ### 信件內容
    with gr.Group():

        gr.Markdown(
            "## 信件內容"
        )

        subject = gr.Textbox(
            label="信件標題"
        )

        body = gr.Textbox(
            label="信件內文",
            lines=10
        )

    ### 附件區
    with gr.Group():

        gr.Markdown(
            "## 附件上傳"
        )

        with gr.Row():

            image_files = gr.File(
                label="📷 圖片附件",
                file_count="multiple",
                file_types=["image"]
            )

            attachment_files = gr.File(
                label="📎 其他附件",
                file_count="multiple"
            )

    ### 發送按鈕
    send_btn = gr.Button(
        "📨 發送系統訊息",
        variant="primary",
        size="lg"
    )

    result = gr.Textbox(
        label="執行結果",
        lines=5
    )

    ### Copyright
    gr.Markdown(
        """
---

<center>

Copyright © 2026 Wei-Cheng Chen

</center>
"""
    )

    ### Event
    unlock_btn.click(
        fn=unlock_password,
        outputs=app_password
    )  # 點擊按鈕後，顯示密碼欄位

    send_btn.click(
        fn=send_email,
        inputs=[
            from_address,
            app_password,
            to_addresses,
            subject,
            body,
            image_files,
            attachment_files
        ],
        outputs=result
    )  # 點擊發送按鈕後，執行寄信函式

demo.launch()  # 啟動 Gradio 網頁介面
```

### 檢討

```text
## **最該改的是密碼安全。** (不一定要修改)

現在密碼是從畫面輸入，雖然方便教學，但學生很容易把應用程式密碼截圖、錄影或不小心存進程式碼。比較好的做法是支援 `.env`，畫面只讓學生選「使用環境變數」或「手動輸入」。

## **收件人格式要檢查。**

現在只用逗號切開，萬一學生輸入： abc@gmail.com，test@gmail.com


中文逗號就會失敗。可以把 `，` 自動轉成 `,`，再加上簡單 Email 格式檢查。

## **寄送結果可以更細。**

現在是一次寄給全部收件人。若其中一個信箱有問題，學生會比較難知道是哪一個。教學上可以改成「逐一寄送」，最後顯示成功幾封、失敗幾封。

## **介面可以加信件預覽。**

學生按下「發送」前，先按「預覽信件」，看到寄件人、收件人、標題、內文、附件數量。這個很有用，因為寄信最常出錯的不是程式，是內容沒檢查。

## **檔案大小要限制。**

Gmail 附件有大小限制，Gradio 也可能卡住。可以在送出前檢查總附件大小，例如超過 20MB 就提醒。

```
