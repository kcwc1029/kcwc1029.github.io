import random
import gradio as gr


# 遊戲主函式
def play_game(user_choice, win_count, lose_count, draw_count):
    choices = ["石頭", "剪刀", "布"]

    computer_choice = random.choice(choices)

    result_message = ""

    # while 用來持續驗證輸入
    while user_choice not in choices:
        return (
            "請輸入：石頭、剪刀、布",
            win_count,
            lose_count,
            draw_count,
        )

    # 判斷勝負
    if user_choice == computer_choice:
        draw_count += 1
        result_message = "平手！"

    elif (
        (user_choice == "石頭" and computer_choice == "剪刀")
        or (user_choice == "剪刀" and computer_choice == "布")
        or (user_choice == "布" and computer_choice == "石頭")
    ):
        win_count += 1
        result_message = "你贏了！"

    else:
        lose_count += 1
        result_message = "你輸了！"

    message = (
        f"你出：{user_choice}\n"
        f"電腦出：{computer_choice}\n\n"
        f"{result_message}\n\n"
        f"目前戰績：\n"
        f"勝利：{win_count} 場\n"
        f"失敗：{lose_count} 場\n"
        f"平手：{draw_count} 場"
    )

    return message, win_count, lose_count, draw_count


# 重置遊戲
def reset_game():
    return (
        "遊戲已重置！",
        0,
        0,
        0,
    )


with gr.Blocks() as demo:
    gr.Markdown("# 石頭剪刀布")
    gr.Markdown("利用 while 驗證輸入是否合法。")

    # 狀態保存
    win_state = gr.State(0)
    lose_state = gr.State(0)
    draw_state = gr.State(0)

    user_input = gr.Textbox(
        label="請輸入 石頭 / 剪刀 / 布"
    )

    output = gr.Textbox(
        label="遊戲結果",
        lines=10
    )

    play_btn = gr.Button("開始猜拳")
    reset_btn = gr.Button("重置戰績")

    play_btn.click(
        fn=play_game,
        inputs=[
            user_input,
            win_state,
            lose_state,
            draw_state,
        ],
        outputs=[
            output,
            win_state,
            lose_state,
            draw_state,
        ],
    )

    reset_btn.click(
        fn=reset_game,
        inputs=[],
        outputs=[
            output,
            win_state,
            lose_state,
            draw_state,
        ],
    )

demo.launch()