from dotenv import load_dotenv
from groq import Groq
import gradio as gr

# 讀取 .env
load_dotenv()

client = Groq()


def chat_with_groq(message, history):
    messages = [
        {
            "role": "system",
            "content": "你是一位親切、清楚、適合教學的 AI 助手，請使用繁體中文回答。",
        }
    ]

    # 加入歷史對話
    for user_msg, assistant_msg in history:
        messages.append({
            "role": "user",
            "content": user_msg
        })
        messages.append({
            "role": "assistant",
            "content": assistant_msg
        })

    # 加入目前使用者輸入
    messages.append({
        "role": "user",
        "content": message
    })

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
    )

    response = ""

    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content
        yield response


# demo = gr.ChatInterface(
#     fn=chat_with_groq,
#     title="Groq AI 聊天機器人",
#     description="使用 llama-3.1-8b-instant，適合低成本、大量 API 呼叫測試。",
# )
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🤖 Groq AI 聊天機器人")

    gr.ChatInterface(
        fn=chat_with_groq,
        title="Groq AI",
        description="使用 llama-3.1-8b-instant",
    )

demo.launch()