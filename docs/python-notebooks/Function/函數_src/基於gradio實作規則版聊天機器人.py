import gradio as gr


def reply_greeting(message):
    if "你好" in message or "嗨" in message or "hello" in message.lower():
        return "你好呀，我是你的 AI 小助理。"


def reply_food(message):
    if "吃什麼" in message or "晚餐" in message or "午餐" in message:
        return "我推薦你吃滷肉飯、鍋燒意麵或雞排便當。"


def reply_weather(message):
    if "天氣" in message or "下雨" in message:
        return "我現在還不能查即時天氣，但你可以記得帶傘。"


def reply_study(message):
    if "讀書" in message or "考試" in message or "作業" in message:
        return "可以先把任務切成 25 分鐘一段，會比較不痛苦。"


def get_bot_reply(message):
    replies = [
        reply_greeting(message),
        reply_food(message),
        reply_weather(message),
        reply_study(message)
    ]

    for reply in replies:
        if reply is not None:
            return reply

    return "這題我還不太會回答，但你可以換個方式問我。"


def chat(message, history):
    if message.strip().lower() == "q":
        return "下次再聊！"

    return get_bot_reply(message)


demo = gr.ChatInterface(
    fn=chat,
    title="規則版 AI 聊天機器人",
    description="輸入你好、吃什麼、天氣、讀書、考試、作業等關鍵字，機器人會依照規則回覆。",
    textbox=gr.Textbox(
        placeholder="請輸入訊息，例如：今天晚餐吃什麼？",
        container=False,
        scale=7
    )
)

demo.launch()