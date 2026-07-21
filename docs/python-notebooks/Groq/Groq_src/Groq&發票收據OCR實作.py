from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
import gradio as gr
import base64
import csv
import json
import re

load_dotenv()
client = Groq()

CSV_PATH = Path("../Groq_datasets/發票收據.csv")

FIELDNAMES = [
    "文件類型",
    "發票號碼",
    "店家名稱",
    "統一編號",
    "日期",
    "總金額",
]


def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_json(text):
    text = (text or "").strip()

    # 移除 ```json ... ``` 這種格式
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    # 從回覆中抓出 JSON
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    return json.loads(text)


def save_to_csv(row):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    need_header = (not CSV_PATH.exists()) or CSV_PATH.stat().st_size == 0

    # 避免手動建立 CSV 時，最後一行沒有換行，導致資料接在標題後面
    if CSV_PATH.exists() and CSV_PATH.stat().st_size > 0:
        with open(CSV_PATH, "rb+") as f:
            f.seek(-1, 2)
            last_char = f.read(1)
            if last_char not in [b"\n", b"\r"]:
                f.write(b"\n")

    with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

        if need_header:
            writer.writeheader()

        writer.writerow(row)


def analyze_and_save(image_path):
    if image_path is None:
        return {"錯誤": "請先上傳圖片"}, "尚未寫入 CSV"

    image_base64 = image_to_base64(image_path)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "你是發票與收據資訊擷取助手。只能輸出合法 JSON，不要使用 Markdown，不要加任何解釋。",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
請分析圖片中的發票或收據，擷取以下欄位。

請只輸出 JSON：

{
  "文件類型": "",
  "發票號碼": "",
  "店家名稱": "",
  "統一編號": "",
  "日期": "",
  "總金額": ""
}

規則：
1. 文件類型只能填「發票」或「收據」
2. 日期請盡量轉成 YYYY-MM-DD
3. 總金額只填數字，不要加元
4. 看不到的欄位請填空字串
5. 不要輸出 JSON 以外的任何文字
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            },
        ],
        temperature=0,
        max_completion_tokens=512,
    )

    result_text = response.choices[0].message.content or ""

    try:
        data = extract_json(result_text)
    except Exception as e:
        return {
            "錯誤": "JSON 解析失敗",
            "原因": str(e),
            "Groq原始回覆": result_text,
        }, "沒有寫入 CSV"

    row = {
        "文件類型": data.get("文件類型", ""),
        "發票號碼": data.get("發票號碼", ""),
        "店家名稱": data.get("店家名稱", ""),
        "統一編號": data.get("統一編號", ""),
        "日期": data.get("日期", ""),
        "總金額": data.get("總金額", ""),
    }

    save_to_csv(row)

    return row, f"已寫入：{CSV_PATH}"


with gr.Blocks() as demo:
    gr.Markdown("# 發票與收據 AI 辨識系統")
    gr.Markdown("上傳發票或收據圖片，按下按鈕後，Groq 會辨識欄位並寫入 CSV。")

    image_input = gr.Image(
        label="上傳發票或收據圖片",
        type="filepath"
    )

    btn = gr.Button("辨識並寫入 CSV")

    result_output = gr.JSON(label="辨識結果")
    csv_output = gr.Textbox(label="CSV 儲存位置")

    btn.click(
        fn=analyze_and_save,
        inputs=image_input,
        outputs=[result_output, csv_output]
    )

demo.launch(theme=gr.themes.Soft())