import gradio as gr


def calculate_ticket(age, is_student):
    # 只要小於 6 歲「或」大於等於 65 歲，就能買優待票
    if age < 6 or age >= 65:
        return "您可以購買優待票：150 元"

    # 如果不是優待身分，但身分是學生
    elif is_student == "Y":
        return "您可以購買學生票：200 元"

    # 其他情況都是全票
    else:
        return "全票：250 元"


with gr.Blocks() as demo:
    gr.Markdown("# 電影票價計算機")
    gr.Markdown("請輸入年齡，並選擇是否為學生。")

    age_input = gr.Number(
        label="請輸入您的年齡",
        value=18,
        precision=0
    )

    student_input = gr.Radio(
        choices=["Y", "N"],
        label="您是學生嗎？",
        value="N"
    )

    btn = gr.Button("計算票價")

    result_output = gr.Textbox(
        label="計算結果"
    )

    btn.click(
        fn=calculate_ticket,
        inputs=[age_input, student_input],
        outputs=result_output
    )


demo.launch()