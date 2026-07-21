import time
import gradio as gr


TARGET_TEXT = "python 很有趣"


# 開始挑戰
def start_game():
    start_time = time.time()

    message = (
        "打字挑戰開始！\n\n"
        f"請輸入以下文字：\n"
        f"{TARGET_TEXT}"
    )

    return start_time, message


# 檢查輸入
def check_typing(user_input, start_time):
    result = ""

    # while：只要還沒輸入正確，就持續挑戰
    while user_input != TARGET_TEXT:

        # 空白輸入
        if user_input.strip() == "":
            return (
                start_time,
                "你還沒輸入內容！"
            )

        return (
            start_time,
            "打錯了！請再試一次！"
        )

    end_time = time.time()

    total_time = round(end_time - start_time, 2)

    result += (
        "挑戰成功！\n\n"
        f"你輸入了正確文字：\n"
        f"{TARGET_TEXT}\n\n"
        f"花費時間：{total_time} 秒"
    )

    return None, result


with gr.Blocks() as demo:
    gr.Markdown("# 打字速度挑戰")
    gr.Markdown("利用 while 模擬『輸入正確前持續挑戰』。")

    start_time_state = gr.State(None)

    output = gr.Textbox(
        label="遊戲訊息",
        lines=10
    )

    user_input = gr.Textbox(
        label="請輸入文字"
    )

    start_btn = gr.Button("開始挑戰")
    submit_btn = gr.Button("送出答案")

    # 開始遊戲
    start_btn.click(
        fn=start_game,
        inputs=[],
        outputs=[
            start_time_state,
            output
        ]
    )

    # 檢查答案
    submit_btn.click(
        fn=check_typing,
        inputs=[
            user_input,
            start_time_state
        ],
        outputs=[
            start_time_state,
            output
        ]
    )

demo.launch()