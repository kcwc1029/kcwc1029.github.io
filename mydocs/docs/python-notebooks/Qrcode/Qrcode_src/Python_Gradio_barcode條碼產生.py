import random
import re
from pathlib import Path

import gradio as gr
import barcode
from barcode.writer import ImageWriter


# 儲存本次程式執行期間產生過的 Code128，避免重複
used_codes = set()


def get_downloads_folder():
    """取得使用者電腦的 Downloads 資料夾，不寫死 Windows 路徑。"""
    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)
    return downloads


def clean_filename(text):
    """移除檔名不允許的字元。"""
    text = text.strip().upper()
    text = re.sub(r'[\\/:*?"<>|]', "_", text)
    text = re.sub(r"\s+", "_", text)
    return text


def check_product_name(product_name):
    """檢查商品名稱。"""
    if not product_name or not product_name.strip():
        return False, "錯誤：商品名稱不可以空白"

    if not re.fullmatch(r"[A-Za-z0-9 _-]+", product_name.strip()):
        return False, "錯誤：商品名稱只能包含英文、數字、空白、底線或減號"

    return True, ""


def check_code128(code_text):
    """檢查 Code128 內容是否為 12 位數字。"""
    if not re.fullmatch(r"\d{12}", code_text.strip()):
        return False, "錯誤：Code128 內容必須是 12 位數字"

    return True, ""


def random_code128():
    """隨機產生本次程式執行期間不重複的 12 位數字。"""
    max_count = 10**12

    if len(used_codes) >= max_count:
        return "", "錯誤：可產生的條碼已用完"

    while True:
        code = str(random.randint(0, 999999999999)).zfill(12)

        if code not in used_codes:
            used_codes.add(code)
            return code, f"成功隨機生成 Code128：{code}"


def generate_barcode(product_name, code_text):
    """生成 Code128 條碼圖片。"""
    product_name = product_name.strip()
    code_text = code_text.strip()

    ok, message = check_product_name(product_name)
    if not ok:
        return None, message

    ok, message = check_code128(code_text)
    if not ok:
        return None, message

    try:
        safe_product_name = clean_filename(product_name)
        downloads_folder = get_downloads_folder()

        base_name = f"{safe_product_name}_{code_text}"
        file_path = downloads_folder / base_name

        # 避免覆蓋舊檔案
        counter = 1
        while file_path.with_suffix(".png").exists():
            file_path = downloads_folder / f"{base_name}_{counter}"
            counter += 1

        Code128 = barcode.get_barcode_class("code128")

        barcode_image = Code128(
            code_text,
            writer=ImageWriter()
        )

        saved_path = barcode_image.save(
            str(file_path),
            options={
                "module_width": 0.35,     # 條碼線條寬度
                "module_height": 18,      # 條碼高度
                "font_size": 18,          # 底下數字大小
                "text_distance": 6,       # 數字與條碼距離
                "quiet_zone": 2,          # 左右留白
                "dpi": 300,               # 圖片品質
            }
        )

        return saved_path, f"成功生成條碼圖片：{saved_path}"

    except Exception as error:
        return None, f"條碼生成失敗：{error}"


with gr.Blocks(title="Code128 條碼產生器") as demo:
    gr.Markdown("# Code128 條碼產生器")
    gr.Markdown("輸入英文商品名稱與 12 位數字，或直接隨機生成一組 Code128。")

    with gr.Row():
        with gr.Column(scale=1):
            product_name_input = gr.Textbox(
                label="英文商品名稱",
                placeholder="例如：COKE",
            )

            code_input = gr.Textbox(
                label="Code128 內容（12 位數字）",
                placeholder="例如：471123456789",
            )

            with gr.Row():
                random_button = gr.Button("隨機生成 Code128")
                generate_button = gr.Button("生成條碼", variant="primary")

            status_output = gr.Textbox(
                label="狀態訊息",
                interactive=False,
            )

        with gr.Column(scale=1):
            image_output = gr.Image(
                label="條碼圖片預覽",
                type="filepath",
            )

    random_button.click(
        fn=random_code128,
        inputs=[],
        outputs=[code_input, status_output],
    )

    generate_button.click(
        fn=generate_barcode,
        inputs=[product_name_input, code_input],
        outputs=[image_output, status_output],
    )


if __name__ == "__main__":
    demo.launch(allowed_paths=[str(get_downloads_folder())])