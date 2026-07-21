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


def analyze_tarot(image: np.ndarray, question: str, spread_type: str, reading_style: str) -> str:
    if image is None:
        return "請先上傳一張塔羅牌照片。"

    if not question.strip():
        question = "請根據這張牌，給我一段適合現在狀態的提醒。"

    # Gradio 上傳進來是 RGB
    image_rgb = image

    # RGB → BGR，交給 OpenCV 處理
    image_bgr = cv2.cvtColor(
        image_rgb,
        cv2.COLOR_RGB2BGR,
    )

    # 壓縮圖片，避免手機原圖太大
    image_bgr = resize_image(
        image_bgr,
        max_size=1024,
    )

    # BGR → RGB，再轉 PIL 給 Gemini
    image_rgb = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2RGB,
    )

    pil_image = Image.fromarray(image_rgb)

    prompt = f"""
你是一位溫柔、有故事感，但不會恐嚇人的 AI 塔羅解牌老師。

請根據使用者上傳的塔羅牌圖片進行分析。

使用者問題：
{question}

牌陣類型：
{spread_type}

解讀風格：
{reading_style}

請用繁體中文回答，格式如下：

## 牌面辨識
請盡量辨識圖片中的塔羅牌名稱。
如果看不清楚，請誠實說「無法完全確認」，並改用畫面元素分析。

## 畫面元素觀察
請描述你看到的主要符號、人物、顏色、姿勢、方向、物件。
例如：杯子、寶劍、權杖、錢幣、太陽、月亮、人物表情等。

## 這張牌可能代表什麼
請用容易懂的方式解釋這張牌的核心含義。

## 對問題的解讀
請結合使用者問題與牌面，給出一段具體解讀。
不要講得太玄，也不要保證一定會發生。

## 行動建議
請給 3 個具體建議。
例如：先觀察、主動溝通、整理情緒、暫緩決定、設定界線等。

## 小提醒
請提醒使用者：
塔羅解讀適合當作自我整理與反思工具，不是絕對預言，也不能取代醫療、法律、財務等專業建議。
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
    fn=analyze_tarot,
    inputs=[
        gr.Image(
            label="上傳塔羅牌照片",
            type="numpy",
        ),
        gr.Textbox(
            label="想問的問題",
            placeholder="例如：我跟對方接下來的關係會如何？",
            lines=3,
        ),
        gr.Dropdown(
            label="牌陣類型",
            choices=[
                "單張牌",
                "三張牌：過去 / 現在 / 未來",
                "三張牌：情況 / 阻礙 / 建議",
                "自由解讀",
            ],
            value="單張牌",
        ),
        gr.Dropdown(
            label="解讀風格",
            choices=[
                "溫柔療癒",
                "直接犀利",
                "像朋友聊天",
                "神秘儀式感",
                "理性分析",
            ],
            value="溫柔療癒",
        ),
    ],
    outputs=gr.Markdown(
        label="塔羅解讀結果",
    ),
    title="OpenCV + Gemini AI 塔羅解牌師",
    description="""
上傳一張塔羅牌照片，輸入你想問的問題，AI 會嘗試辨識牌面並給出解讀。

這個專案適合練習：OpenCV 圖片前處理、Gemini 圖像理解、Gradio 介面設計。
""",
)


if __name__ == "__main__":
    demo.launch()