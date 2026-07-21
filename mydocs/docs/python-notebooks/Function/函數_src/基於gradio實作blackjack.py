import random
import gradio as gr


def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)


def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0

    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)

    return sum(cards)


def display_score(score):
    if score == 0:
        return "Blackjack"
    return str(score)


def compare_scores(user_score, computer_score):
    if user_score == computer_score:
        return "平手 🙃"
    elif computer_score == 0:
        return "對手有 Blackjack，你輸了 😩"
    elif user_score == 0:
        return "你有 Blackjack，你贏了 😁"
    elif user_score > 21:
        return "你爆牌了，你輸了 😭"
    elif computer_score > 21:
        return "對手爆牌了，你贏了 😀"
    elif user_score > computer_score:
        return "你贏了 😊"
    else:
        return "你輸了 😢"


def start_game():
    user_cards = [deal_card(), deal_card()]
    computer_cards = [deal_card(), deal_card()]

    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    if user_score == 0 or computer_score == 0:
        result = compare_scores(user_score, computer_score)
        message = "遊戲結束！"
        is_game_over = True
        computer_display = f"{computer_cards}，分數：{display_score(computer_score)}"
    else:
        result = ""
        message = "遊戲開始！你可以選擇要牌或停牌。"
        is_game_over = False
        computer_display = f"[{computer_cards[0]}, ?]，第一張牌：{computer_cards[0]}"

    user_display = f"{user_cards}，分數：{display_score(user_score)}"

    return (
        user_cards,
        computer_cards,
        is_game_over,
        user_display,
        computer_display,
        message,
        result,
    )


def hit_card(user_cards, computer_cards, is_game_over):
    if not user_cards or not computer_cards:
        return (
            user_cards,
            computer_cards,
            is_game_over,
            "請先按「開始新遊戲」。",
            "",
            "還沒有開始遊戲。",
            "",
        )

    if is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        return (
            user_cards,
            computer_cards,
            is_game_over,
            f"{user_cards}，分數：{display_score(user_score)}",
            f"{computer_cards}，分數：{display_score(computer_score)}",
            "這局已經結束，請重新開始新遊戲。",
            compare_scores(user_score, computer_score),
        )

    user_cards.append(deal_card())
    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    if user_score == 0 or user_score > 21:
        is_game_over = True
        result = compare_scores(user_score, computer_score)
        message = "遊戲結束！"
        computer_display = f"{computer_cards}，分數：{display_score(computer_score)}"
    else:
        result = ""
        message = "你抽了一張牌。可以繼續要牌，或選擇停牌。"
        computer_display = f"[{computer_cards[0]}, ?]，第一張牌：{computer_cards[0]}"

    user_display = f"{user_cards}，分數：{display_score(user_score)}"

    return (
        user_cards,
        computer_cards,
        is_game_over,
        user_display,
        computer_display,
        message,
        result,
    )


def stand_card(user_cards, computer_cards, is_game_over):
    if not user_cards or not computer_cards:
        return (
            user_cards,
            computer_cards,
            is_game_over,
            "請先按「開始新遊戲」。",
            "",
            "還沒有開始遊戲。",
            "",
        )

    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    if is_game_over:
        result = compare_scores(user_score, computer_score)
        return (
            user_cards,
            computer_cards,
            is_game_over,
            f"{user_cards}，分數：{display_score(user_score)}",
            f"{computer_cards}，分數：{display_score(computer_score)}",
            "這局已經結束，請重新開始新遊戲。",
            result,
        )

    while computer_score != 0 and computer_score < 17 and user_score <= 21:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    is_game_over = True
    result = compare_scores(user_score, computer_score)

    user_display = f"{user_cards}，分數：{display_score(user_score)}"
    computer_display = f"{computer_cards}，分數：{display_score(computer_score)}"
    message = "你選擇停牌，莊家回合結束。"

    return (
        user_cards,
        computer_cards,
        is_game_over,
        user_display,
        computer_display,
        message,
        result,
    )


with gr.Blocks() as demo:
    gr.Markdown("# Blackjack 21 點遊戲")
    gr.Markdown("目標是讓自己的手牌盡量接近 21 點，但不能超過。A 可以算 11 點，爆牌時會自動改成 1 點。")

    user_cards_state = gr.State([])
    computer_cards_state = gr.State([])
    game_over_state = gr.State(True)

    start_btn = gr.Button("開始新遊戲", variant="primary")

    with gr.Row():
        hit_btn = gr.Button("要牌")
        stand_btn = gr.Button("停牌")

    user_output = gr.Textbox(label="你的手牌", interactive=False)
    computer_output = gr.Textbox(label="莊家的手牌", interactive=False)
    message_output = gr.Textbox(label="遊戲訊息", lines=3, interactive=False)
    result_output = gr.Textbox(label="遊戲結果", interactive=False)

    start_btn.click(
        fn=start_game,
        inputs=[],
        outputs=[
            user_cards_state,
            computer_cards_state,
            game_over_state,
            user_output,
            computer_output,
            message_output,
            result_output,
        ],
    )

    hit_btn.click(
        fn=hit_card,
        inputs=[
            user_cards_state,
            computer_cards_state,
            game_over_state,
        ],
        outputs=[
            user_cards_state,
            computer_cards_state,
            game_over_state,
            user_output,
            computer_output,
            message_output,
            result_output,
        ],
    )

    stand_btn.click(
        fn=stand_card,
        inputs=[
            user_cards_state,
            computer_cards_state,
            game_over_state,
        ],
        outputs=[
            user_cards_state,
            computer_cards_state,
            game_over_state,
            user_output,
            computer_output,
            message_output,
            result_output,
        ],
    )

demo.launch()