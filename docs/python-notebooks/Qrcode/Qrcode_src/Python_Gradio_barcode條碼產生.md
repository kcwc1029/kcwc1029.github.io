```py
import random
import re
from pathlib import Path

import barcode
import gradio as gr
from barcode.writer import ImageWriter


### 已使用的條碼編號
# 儲存本次程式執行期間產生過的 Code128
# 避免隨機產生重複的條碼編號
used_codes = set()


### 取得下載資料夾
def get_downloads_folder():
    """取得使用者電腦的 Downloads 資料夾。"""

    downloads_folder = Path.home() / "Downloads"  # 組合使用者的 Downloads 資料夾路徑
    downloads_folder.mkdir(parents=True, exist_ok=True)  # 若資料夾不存在則自動建立

    return downloads_folder


### 清理檔案名稱
def clean_filename(text):
    """移除檔名不允許使用的字元。"""

    text = text.strip().upper()  # 移除前後空白並轉換成大寫
    text = re.sub(r'[\\/:*?"<>|]', "_", text)  # 將檔名不允許的字元替換成底線
    text = re.sub(r"\s+", "_", text)  # 將一個以上的空白替換成底線

    return text


### 檢查商品名稱
def check_product_name(product_name):
    """檢查商品名稱格式是否正確。"""

    # 商品名稱不可以是空字串或只有空白
    if not product_name or not product_name.strip():
        return False, "錯誤：商品名稱不可以空白"

    # 商品名稱只能包含英文、數字、空白、底線或減號
    if not re.fullmatch(r"[A-Za-z0-9 _-]+", product_name.strip()):
        return False, "錯誤：商品名稱只能包含英文、數字、空白、底線或減號"

    return True, ""


### 檢查 Code128 內容
def check_code128(code_text):
    """檢查 Code128 內容是否為 12 位數字。"""

    # Code128 內容必須剛好是 12 位數字
    if not re.fullmatch(r"\d{12}", code_text.strip()):
        return False, "錯誤：Code128 內容必須是 12 位數字"

    return True, ""


### 隨機產生 Code128
def random_code128():
    """隨機產生本次程式執行期間不重複的 12 位數字。"""

    max_count = 10**12  # 12 位數字最多可以產生的組合數量

    # 檢查所有可能的條碼編號是否已經使用完畢
    if len(used_codes) >= max_count:
        return "", "錯誤：可產生的條碼已用完"

    while True:
        # 隨機產生 0 到 999999999999 之間的數字
        # zfill(12) 會在數字左側補 0，確保總長度為 12 位
        code_text = str(random.randint(0, 999999999999)).zfill(12)

        # 確認條碼編號尚未使用過
        if code_text not in used_codes:
            used_codes.add(code_text)

            return code_text, f"成功隨機生成 Code128：{code_text}"


### 產生 Code128 條碼
def generate_barcode(product_name, code_text):
    """產生 Code128 條碼圖片並儲存到 Downloads 資料夾。"""

    product_name = product_name.strip()  # 移除商品名稱前後空白
    code_text = code_text.strip()  # 移除條碼內容前後空白

    ### 驗證商品名稱
    is_valid, message = check_product_name(product_name)

    if not is_valid:
        return None, message

    ### 驗證 Code128 內容
    is_valid, message = check_code128(code_text)

    if not is_valid:
        return None, message

    try:
        ### 準備輸出檔案路徑
        safe_product_name = clean_filename(product_name)  # 建立可以安全使用的商品檔名
        downloads_folder = get_downloads_folder()  # 取得 Downloads 資料夾

        base_name = f"{safe_product_name}_{code_text}"  # 組合商品名稱與條碼編號
        file_path = downloads_folder / base_name  # 組合條碼圖片儲存路徑

        ### 避免覆蓋已存在的圖片
        counter = 1

        while file_path.with_suffix(".png").exists():
            file_path = downloads_folder / f"{base_name}_{counter}"
            counter += 1

        ### 建立 Code128 類別
        Code128 = barcode.get_barcode_class("code128")

        ### 建立 PNG 條碼物件
        # ImageWriter() 用來將條碼輸出為 PNG 圖片
        barcode_image = Code128(
            code_text,
            writer=ImageWriter()
        )

        ### 儲存 PNG 條碼圖片
        # save() 不需要加副檔名
        # python-barcode 會自動建立 .png 檔案
        saved_path = barcode_image.save(
            str(file_path),
            options={
                "module_width": 0.35,  # 條碼線條寬度
                "module_height": 18,  # 條碼高度
                "font_size": 18,  # 條碼下方文字大小
                "text_distance": 6,  # 文字與條碼之間的距離
                "quiet_zone": 2,  # 條碼左右兩側留白
                "dpi": 300,  # 圖片解析度
            }
        )

        return saved_path, f"成功生成條碼圖片：{saved_path}"

    except Exception as error:
        return None, f"條碼生成失敗：{error}"


### 建立 Gradio 操作介面
with gr.Blocks(title="Code128 條碼產生器") as demo:
    gr.Markdown("# Code128 條碼產生器")
    gr.Markdown("輸入英文商品名稱與 12 位數字，或直接隨機生成一組 Code128。")

    ### 輸入與輸出區域
    with gr.Row():

        ### 左側輸入區域
        with gr.Column(scale=1):
            product_name_input = gr.Textbox(
                label="英文商品名稱",
                placeholder="例如：COKE",
            )

            code_input = gr.Textbox(
                label="Code128 內容（12 位數字）",
                placeholder="例如：471123456789",
            )

            ### 操作按鈕
            with gr.Row():
                random_button = gr.Button("隨機生成 Code128")
                generate_button = gr.Button(
                    "生成條碼",
                    variant="primary",
                )

            status_output = gr.Textbox(
                label="狀態訊息",
                interactive=False,
            )

        ### 右側圖片預覽區域
        with gr.Column(scale=1):
            image_output = gr.Image(
                label="條碼圖片預覽",
                type="filepath",
            )

    ### 隨機產生條碼按鈕事件
    random_button.click(
        fn=random_code128,
        inputs=[],
        outputs=[
            code_input,
            status_output,
        ],
    )

    ### 產生條碼按鈕事件
    generate_button.click(
        fn=generate_barcode,
        inputs=[
            product_name_input,
            code_input,
        ],
        outputs=[
            image_output,
            status_output,
        ],
    )


### 啟動 Gradio 網頁
if __name__ == "__main__":
    downloads_folder = get_downloads_folder()

    demo.launch(
        allowed_paths=[str(downloads_folder)]
    )
```

### 提示詞：

```text
# Python + Gradio 條碼產生器 小實作

請幫我使用 Python + Gradio 製作一個「Code128 條碼產生器」。
請直接提供完整版本程式碼，不要只給片段。

## 專案目標

使用者可以：
1. 輸入英文商品名稱
2. 輸入 Code128 條碼內容
3. 或按下按鈕自動隨機生成
4. 最後按下「生成條碼」
5. 自動輸出 PNG 條碼圖片

## GUI 介面需求

請使用 Gradio 製作介面。介面需要包含：
* 英文商品名稱輸入框
* Code128 內容輸入框
* 「隨機生成 Code128」按鈕
* 「生成條碼」按鈕
* 條碼圖片預覽區
* 狀態訊息區(例如：成功生成、輸入錯誤等)

請讓介面有基本排版，不要全部擠在一起。

## Code128 規則

請使用：barcode.get_barcode_class("code128")


請注意：

- Code128 可以支援英文與數字
- 本次練習請限制為「12 位數字」
- 請檢查輸入是否合法
- 若輸入錯誤，請在介面顯示錯誤訊息

不要讓程式直接崩潰。

## 隨機生成功能

當使用者按下：「隨機生成 Code128」。系統需要：

- 自動產生一組 12 位數字
- 本次程式執行期間不可重複
- 自動填入輸入框
- 請自行設計避免重複的方法。

## 條碼圖片生成需求

當使用者按下：「生成條碼」。程式需要：

- 使用 python-barcode 生成 Code128
- 使用 `ImageWriter()` 輸出 PNG
- 自動預覽條碼圖片

請使用：from barcode.writer import ImageWriter


## 檔案儲存需求

生成的 PNG 圖片：

- 請自動儲存到使用者電腦預設下載資料夾
- 不要寫死 Windows 絕對路徑
- 請使用 Python 標準方式取得 Downloads 路徑

## 檔名規則

檔名需要包含：

- 英文商品名稱
- Code128 內容

例如： COKE_471123456789.png


避免檔案被覆蓋。

若檔名有非法字元，請自行處理。


## 錯誤處理需求

以下情況請顯示錯誤訊息：

- 商品名稱為空
- Code128 內容不是 12 位數字
- 出現非法字元
- 條碼生成失敗

請不要讓整個程式直接中斷。



## 套件需求

請使用：

- gradio
- python-barcode
- pillow

```
