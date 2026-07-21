import os
import base64
from pathlib import Path

import cv2
import gradio as gr
import numpy as np
from dotenv import load_dotenv
from groq import Groq


# =========================
# 讀取 API Key
# =========================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY
)


# =========================
# 模型設定
# =========================

MODEL_OPTIONS = {
    "Llama 4 Scout": "meta-llama/llama-4-scout-17b-16e-instruct",
    "Qwen3.6 27B": "qwen/qwen3.6-27b",
}


# =========================
# OpenCV 圖片預處理
# =========================

def preprocess_image(image):
    if image is None:
        raise ValueError("請先上傳圖片")

    # Gradio 上傳進來是 RGB
    # OpenCV 使用 BGR
    image = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2BGR
    )

    # 放大圖片，讓 K 線、價格、成交量更清楚
    image = cv2.resize(
        image,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    # 銳化
    sharpen_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    image = cv2.filter2D(
        image,
        -1,
        sharpen_kernel
    )

    output_path = "processed_stock_chart.jpg"

    cv2.imwrite(
        output_path,
        image
    )

    return output_path


# =========================
# 圖片轉 Base64
# =========================

def image_to_base64(image_path):
    image_bytes = Path(image_path).read_bytes()

    encoded = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    return f"data:image/jpeg;base64,{encoded}"


# =========================
# Groq 股票分析
# =========================

def analyze_stock_chart(image, model_name, stock_name, user_question):
    try:
        if image is None:
            return "請先上傳股票技術線圖截圖。"

        if not GROQ_API_KEY:
            return "找不到 GROQ_API_KEY，請先在 .env 設定 API Key。"

        processed_path = preprocess_image(image)
        image_base64 = image_to_base64(processed_path)

        model_id = MODEL_OPTIONS[model_name]

        prompt = f"""
你是一位專業但保守的股票技術分析師。

使用者上傳的是個股技術面截圖，可能包含：
K 線圖、均線、成交量、MACD、KD、RSI、布林通道、支撐壓力、價格區間等資訊。

請只根據圖片中看得到的資訊分析。
不要假裝知道圖片以外的基本面、新聞、財報或即時股價。
如果價格數字看不清楚，請明確說「圖片價格軸不清楚，只能估計區間」。

個股名稱或代號：
{stock_name if stock_name else "使用者未提供"}

使用者補充問題：
{user_question if user_question else "無"}

請用繁體中文回答。

請嚴格按照下面格式回答，每段 3 到 5 句即可，不要重複句子：

一、圖表觀察
說明目前看到的 K 線型態、均線位置、價格相對位置。

二、目前趨勢
判斷偏多、偏空或盤整，並說明理由。

三、成交量觀察
說明量能是否放大或縮小，買盤或賣壓是否明顯。

四、支撐與壓力區
根據圖片中的價格區間估計：
- 可能支撐區：
- 可能壓力區：

五、操作區間建議
請用條件式寫法，不要直接叫使用者買進或賣出。
例如：
- 若站上某區間，可以觀察偏多延續
- 若跌破某區間，應提高風險控管
- 若靠近支撐但量縮止跌，可列為觀察區
- 若爆量跌破支撐，不宜追價

六、風險提醒
提醒這只是技術面解讀，不是投資保證，也不能取代個人投資決策。

禁止事項：
不要說「一定會漲」
不要說「一定會跌」
不要說「保證獲利」
不要一直重複相同詞語
不要輸出無意義重複句

回答完「六、風險提醒」後，請輸出：
風險提醒結束
"""

        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_base64
                            },
                        },
                    ],
                }
            ],
            temperature=0.2,
            max_tokens=900,
            stop=["風險提醒結束"]
        )

        result = response.choices[0].message.content

        return result

    except Exception as error:
        return f"程式執行時發生錯誤：\n\n{error}"


# =========================
# Gradio 介面
# =========================

with gr.Blocks(
    title="AI 股票技術分析師"
) as demo:

    gr.Markdown(
        """
# AI 股票技術分析師

上傳個股技術線圖截圖，系統會使用 OpenCV 預處理圖片，  
再交給 Groq Vision 模型分析目前趨勢、量能、支撐壓力與操作區間。
"""
    )

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(
                label="上傳股票技術線圖截圖",
                type="numpy"
            )

            model_input = gr.Dropdown(
                choices=list(MODEL_OPTIONS.keys()),
                value="Llama 4 Scout",
                label="選擇 Groq 視覺模型"
            )

            stock_name_input = gr.Textbox(
                label="股票名稱或代號",
                placeholder="例如：台積電 2330"
            )

            question_input = gr.Textbox(
                label="補充問題",
                placeholder="例如：現在適合進場嗎？壓力區大概在哪？",
                lines=3
            )

            analyze_button = gr.Button("開始分析")

        with gr.Column():
            output = gr.Markdown(
                label="分析結果"
            )

    analyze_button.click(
        fn=analyze_stock_chart,
        inputs=[
            image_input,
            model_input,
            stock_name_input,
            question_input,
        ],
        outputs=output
    )


if __name__ == "__main__":
    demo.launch()