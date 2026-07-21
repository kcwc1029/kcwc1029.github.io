import gradio as gr


# 餵食函式
def feed_pet(food, hunger):
    hunger = int(hunger)

    message = ""

    # while：只要還沒吃飽，就繼續餵
    while hunger > 0:

        # 驗證輸入
        if food.strip() == "":
            return (
                "你沒有輸入食物！",
                hunger
            )

        hunger -= 1

        message += (
            f"你餵了寵物：{food}\n"
            f"寵物開心地吃掉了！\n"
            f"目前飢餓值：{hunger}\n\n"
        )

        # Gradio 不能像終端機 while 那樣一直等輸入
        # 所以餵一次就先停止
        break

    # 吃飽了
    if hunger <= 0:
        message += "寵物吃飽了！好幸福～"

    return message, hunger


# 重置
def reset_pet():
    return (
        "寵物肚子餓了，快來餵食！",
        5
    )


with gr.Blocks() as demo:
    gr.Markdown("# 寵物餵食模擬器")
    gr.Markdown("利用 while 模擬『還沒吃飽就繼續餵』的概念。")

    hunger_state = gr.State(5)

    food_input = gr.Textbox(
        label="請輸入食物名稱"
    )

    output = gr.Textbox(
        label="寵物狀態",
        lines=10
    )

    feed_btn = gr.Button("餵食")
    reset_btn = gr.Button("重新開始")

    feed_btn.click(
        fn=feed_pet,
        inputs=[
            food_input,
            hunger_state
        ],
        outputs=[
            output,
            hunger_state
        ]
    )

    reset_btn.click(
        fn=reset_pet,
        inputs=[],
        outputs=[
            output,
            hunger_state
        ]
    )

demo.launch()