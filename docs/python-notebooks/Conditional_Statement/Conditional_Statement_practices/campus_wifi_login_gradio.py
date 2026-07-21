import gradio as gr


def check_wifi(is_login):
    ### 從這裡開始寫


description = """
# Problem. 校園 Wi-Fi 登入

學生是否已登入(is_login)為 True。

接著：

如果已登入  
輸出「成功連接校園網路」

否則  
輸出「請先登入學校帳號」
"""


with gr.Blocks() as demo:
    gr.Markdown(description)

    login_input = gr.Checkbox(
        label="是否已登入學校帳號",
        value=True
    )

    check_button = gr.Button("檢查 Wi-Fi 狀態")

    result_output = gr.Textbox(
        label="系統結果"
    )

    check_button.click(
        fn=check_wifi,
        inputs=login_input,
        outputs=result_output
    )


demo.launch()