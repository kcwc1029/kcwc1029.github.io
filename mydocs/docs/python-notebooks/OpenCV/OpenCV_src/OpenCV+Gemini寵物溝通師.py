import os

import cv2
import gradio as gr
import numpy as np
from dotenv import load_dotenv
from google import genai
from PIL import Image


# =========================
# 讀取 .env
# =========================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("找不到 GEMINI_API_KEY，請確認 .env 是否有設定")


# =========================
# 建立 Gemini Client
# =========================
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.1-flash-lite"


# =========================
# OpenCV 圖片前處理
# =========================
def resize_image(image: np.ndarray, max_size: int = 1024) -> np.ndarray:
    height, width = image.shape[:2]

    if max(height, width) <= max_size:
        return image

    scale = max_size / max(height, width)
    new_width = int(width * scale)
    new_height = int(height * scale)

    return cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA,
    )


def analyze_pet(image: np.ndarray, pet_name: str, tone: str) -> str:
    if image is None:
        return "請先上傳一張寵物照片。"

    if not pet_name.strip():
        pet_name = "毛小孩"

    # Gradio 圖片是 RGB
    image_rgb = image

    # RGB → BGR，讓 OpenCV 處理
    image_bgr = cv2.cvtColor(
        image_rgb,
        cv2.COLOR_RGB2BGR,
    )

    # 壓縮圖片，避免手機原圖太大
    image_bgr = resize_image(
        image_bgr,
        max_size=1024,
    )

    # BGR → RGB，再轉成 PIL 給 Gemini
    image_rgb = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2RGB,
    )

    pil_image = Image.fromarray(image_rgb)

    prompt = f"""
你是一位有趣、溫柔、很會觀察寵物表情的「AI 寵物溝通師」。

請根據圖片中的寵物姿勢、表情、眼神、耳朵、尾巴、環境，模擬牠現在可能想說的話。

寵物名字：{pet_name}
回覆風格：{tone}

請用繁體中文回答，格式如下：

## 我看到的畫面
簡單描述圖片裡的寵物狀態。

## {pet_name} 可能在想
請用第一人稱，模擬寵物正在對主人說話。
語氣要可愛、有趣，但不要太浮誇。

## 主人可以怎麼回應
給 3 個簡單建議，例如陪牠玩、給水、讓牠休息、摸摸牠。

## 小提醒
請提醒使用者：這只是娛樂與陪伴用途，不能取代獸醫診斷。
如果寵物看起來受傷、喘、嘔吐、精神異常，應該找獸醫。
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt,
                pil_image,
            ],
        )

        return response.text

    except Exception as error:
        return f"分析失敗：{error}"


# =========================
# Gradio 介面
# =========================
demo = gr.Interface(
    fn=analyze_pet,
    inputs=[
        gr.Image(
            label="上傳寵物照片",
            type="numpy",
        ),
        gr.Textbox(
            label="寵物名字",
            placeholder="例如：阿柴、咪咪、肉包",
            value="毛小孩",
        ),
        gr.Dropdown(
            label="回覆風格",
            choices=[
                "可愛撒嬌",
                "傲嬌毒舌",
                "溫柔療癒",
                "搞笑吐槽",
                "像小朋友說話",
            ],
            value="可愛撒嬌",
        ),
    ],
    outputs=gr.Markdown(
        label="寵物溝通結果",
    ),
    title="OpenCV + Gemini AI 寵物溝通師",
    description="""
上傳一張狗狗、貓咪或其他寵物照片，AI 會根據牠的表情與姿勢，模擬牠可能想對主人說的話。

這個專案適合用來練習：OpenCV 圖片處理、Gemini 圖像理解、Gradio 介面設計。
""",
)


if __name__ == "__main__":
    demo.launch(share=True)