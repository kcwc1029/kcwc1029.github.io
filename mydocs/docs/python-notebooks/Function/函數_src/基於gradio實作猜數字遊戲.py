import random
import gradio as gr

EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5


def start_game(level):
    answer = random.randint(1, 100)

    if level == "簡單 easy":
        turns = EASY_LEVEL_TURNS
    else:
        turns = HARD_LEVEL_TURNS

    message = f"遊戲開始！我已經想好 1 到 100 的數字。\n你有 {turns} 次機會。"
    return answer, turns, True, message, ""


def check_guess(guess, answer, turns, is_playing):
    if not is_playing:
        return answer, turns, is_playing, "請先按「開始新遊戲」。", ""

    if guess is None:
        return answer, turns, is_playing, "請輸入一個數字。", ""

    if guess < 1 or guess > 100:
        return answer, turns, is_playing, "請輸入 1 到 100 之間的數字。", ""

    turns -= 1

    if guess == answer:
        is_playing = False
        return answer, turns, is_playing, f"你猜對了！答案是 {answer}。", "🎉 勝利"

    if turns == 0:
        is_playing = False
        return answer, turns, is_playing, f"你所有的猜測機會都用完了。正確答案是 {answer}。", "💀 失敗"

    if guess > answer:
        hint = "太高了。"
    else:
        hint = "太低了。"

    message = f"{hint}\n你還剩下 {turns} 次機會，再猜一次。"
    return answer, turns, is_playing, message, ""


with gr.Blocks() as demo:
    gr.Markdown("# 猜數字遊戲")

    gr.Markdown("我會隨機想一個 1 到 100 之間的數字，你要在限定次數內猜中它。")

    answer_state = gr.State(0)
    turns_state = gr.State(0)
    playing_state = gr.State(False)

    level = gr.Radio(
        choices=["簡單 easy", "困難 hard"],
        value="簡單 easy",
        label="選擇難度",
    )

    start_btn = gr.Button("開始新遊戲", variant="primary")

    guess_input = gr.Number(
        label="請輸入你的猜測",
        precision=0,
        minimum=1,
        maximum=100,
    )

    guess_btn = gr.Button("送出猜測")

    message_output = gr.Textbox(
        label="遊戲訊息",
        lines=5,
        interactive=False,
    )

    result_output = gr.Textbox(
        label="遊戲結果",
        interactive=False,
    )

    start_btn.click(
        fn=start_game,
        inputs=level,
        outputs=[answer_state, turns_state, playing_state, message_output, result_output],
    )

    guess_btn.click(
        fn=check_guess,
        inputs=[guess_input, answer_state, turns_state, playing_state],
        outputs=[answer_state, turns_state, playing_state, message_output, result_output],
    )

demo.launch()