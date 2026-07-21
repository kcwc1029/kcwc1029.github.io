import gradio as gr


def check_access(age):
    ### 從這邊開始寫


description = """
# Problem. Discord 身分組驗證

使用者年齡(age)為 19。

接著：

* 如果年齡大於等於 18，輸出「可以進入成人頻道」
* 否則：輸出「限制存取」
"""


with gr.Blocks() as demo:
    gr.Markdown(description)

    age_input = gr.Number(
        label="請輸入年齡",
        value=19,
        precision=0
    )

    check_button = gr.Button("驗證")

    result_output = gr.Textbox(
        label="驗證結果"
    )

    check_button.click(
        fn=check_access,
        inputs=age_input,
        outputs=result_output
    )


demo.launch()