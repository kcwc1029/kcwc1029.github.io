import random
import gradio as gr


def start_game():
    answer = random.randint(1, 100)
    count = 0
    message = "遊戲開始！請輸入 1～100 的數字。"
    return answer, count, message


def guess_number(user_guess, answer, count):
    if answer is None:
        answer = random.randint(1, 100)
        count = 0

    count += 1
    guess = int(user_guess)

    while guess != answer:
        if guess > answer:
            return answer, count, f"你猜 {guess}，太大了！目前猜了 {count} 次"
        else:
            return answer, count, f"你猜 {guess}，太小了！目前猜了 {count} 次"

    return None, 0, f"答對了！答案就是 {answer}，你總共猜了 {count} 次。遊戲結束！"


with gr.Blocks() as demo:
    gr.Markdown("# 猜數字遊戲")
    gr.Markdown("玩家一直猜，猜對才停止。這題很適合練習 while。")

    answer_state = gr.State(None)
    count_state = gr.State(0)

    user_guess = gr.Number(label="請輸入 1～100 的數字", precision=0)
    output = gr.Textbox(label="遊戲結果")

    start_btn = gr.Button("開始新遊戲")
    guess_btn = gr.Button("送出答案")

    start_btn.click(
        fn=start_game,
        inputs=[],
        outputs=[answer_state, count_state, output]
    )

    guess_btn.click(
        fn=guess_number,
        inputs=[user_guess, answer_state, count_state],
        outputs=[answer_state, count_state, output]
    )

demo.launch()