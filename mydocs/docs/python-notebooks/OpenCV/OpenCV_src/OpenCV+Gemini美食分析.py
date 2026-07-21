import os
from pathlib import Path

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
    raise ValueError("找不到 GEMINI_API_KEY，請確認 .env 是否設定正確")


# =========================
# 建立 Gemini Client
# =========================
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.1-flash-lite"


# =========================
# 圖片前處理
# =========================
def resize_image_for_ai(image: np.ndarray, max_size: int = 1024) -> np.ndarray:
    """
    將圖片縮小，避免手機原圖太大。
    max_size 代表圖片最長邊不超過多少像素。
    """
    height, width = image.shape[:2]

    if max(height, width) <= max_size:
        return image

    scale = max_size / max(height, width)

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized_image = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA,
    )

    return resized_image


def analyze_food(image: np.ndarray) -> str:
    """
    接收 Gradio 上傳的圖片，使用 Gemini 分析食物內容。
    """

    if image is None:
        return "請先上傳一張食物照片。"

    # Gradio 進來的圖片是 RGB
    image_rgb = image

    # RGB 轉 BGR，給 OpenCV 處理
    image_bgr = cv2.cvtColor(
        image_rgb,
        cv2.COLOR_RGB2BGR,
    )

    # 壓縮圖片尺寸
    image_bgr = resize_image_for_ai(
        image_bgr,
        max_size=1024,
    )

    # BGR 轉回 RGB，準備轉 PIL 給 Gemini
    image_rgb = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2RGB,
    )

    pil_image = Image.fromarray(image_rgb)

    prompt = """
你是一位親切但專業的 AI 美食分析師。

請根據圖片分析食物內容，並用繁體中文回答。

請依照以下格式輸出：

## 可能的食物內容
請列出你看到的主要食物。

## 熱量粗估
請估算整份餐點大約熱量。
如果無法精準判斷，請用範圍表示。

## 蛋白質來源
請指出圖片中可能的蛋白質來源。

## 減脂適合度
請用 1 到 10 分評估。
1 分代表非常不適合，10 分代表很適合。

## 建議調整
請給 3 個具體建議，例如白飯減半、少喝含糖飲料、增加青菜等。

提醒：
這不是醫療診斷，只能作為飲食參考。
不要假裝能精準知道重量或熱量。
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
    fn=analyze_food,
    inputs=gr.Image(
        label="上傳食物照片",
        type="numpy",
    ),
    outputs=gr.Markdown(
        label="AI 分析結果",
    ),
    title="OpenCV + Gemini AI 美食分析師",
    description="""
上傳一張午餐、便當、飲料或點心照片，AI 會幫你分析食物內容、熱量粗估、蛋白質來源與減脂建議。

建議使用清楚、光線足夠的照片。
""",
    examples=None,
)


if __name__ == "__main__":
    demo.launch(share=True)