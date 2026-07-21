import gradio as gr


def check_battery(battery, is_charging):
    ### 從這裡開始寫


description = """
# Problem. 手機充電提醒系統

手機電量(battery)為 15。

是否正在充電(is_charging)為 False。

接著，如果：

- 電量小於等於 20  
- 且目前沒有充電

則輸出「請立即充電」；否則輸出「目前電量正常」
"""


with gr.Blocks() as demo:
    gr.Markdown(description)

    battery_input = gr.Slider(
        minimum=0,
        maximum=100,
        value=15,
        step=1,
        label="手機電量 (%)"
    )

    charging_input = gr.Checkbox(
        label="是否正在充電",
        value=False
    )

    check_button = gr.Button("檢查電量狀態")

    result_output = gr.Textbox(
        label="系統提醒"
    )

    check_button.click(
        fn=check_battery,
        inputs=[battery_input, charging_input],
        outputs=result_output
    )


demo.launch()