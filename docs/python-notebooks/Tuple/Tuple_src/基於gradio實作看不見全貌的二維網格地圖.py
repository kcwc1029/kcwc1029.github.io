import math
import gradio as gr

TREASURE_LOC = (3, 4)
TRAPS = ((1, 2), (-2, 3), (4, -1))
START_LOC = (0, 0)


def calc_distance(player_loc):
    px, py = player_loc
    tx, ty = TREASURE_LOC
    return math.sqrt((tx - px) ** 2 + (ty - py) ** 2)


def draw_map(player_loc, game_over=False):
    min_x, max_x = -3, 5
    min_y, max_y = -2, 5

    html = """
    <div style="font-family:Arial; line-height:1.6;">
    <h3>🗺️ 迷霧森林地圖</h3>
    <table style="border-collapse:collapse;">
    """

    for y in range(max_y, min_y - 1, -1):
        html += "<tr>"
        for x in range(min_x, max_x + 1):
            loc = (x, y)

            bg = "#1f2937"
            text = "⬛"

            if loc == player_loc:
                bg = "#facc15"
                text = "🧍"
            elif loc == START_LOC:
                bg = "#4ade80"
                text = "🏠"
            elif game_over and loc == TREASURE_LOC:
                bg = "#f59e0b"
                text = "💎"
            elif game_over and loc in TRAPS:
                bg = "#ef4444"
                text = "💀"

            html += f"""
            <td style="
                width:48px;
                height:48px;
                text-align:center;
                border:1px solid #555;
                background:{bg};
                font-size:24px;
            ">{text}</td>
            """

        html += "</tr>"

    html += """
    </table>
    <p>🧍 玩家　🏠 起點　💎 寶藏　💀 陷阱</p>
    <p>遊戲進行中時，寶藏與陷阱會先隱藏。</p>
    </div>
    """

    return html


def start_game():
    player_loc = START_LOC
    distance = calc_distance(player_loc)

    message = f"""
🌲 歡迎來到【迷霧森林尋寶】

你目前的位置：{player_loc}

📡 探測器顯示，你距離寶藏還有 {round(distance, 2)} 步。

請點選方向按鈕移動。
"""

    return player_loc, message, draw_map(player_loc), ""


def move_player(direction, player_loc):
    if player_loc is None:
        player_loc = START_LOC

    x, y = player_loc

    if direction == "上":
        y += 1
    elif direction == "下":
        y -= 1
    elif direction == "左":
        x -= 1
    elif direction == "右":
        x += 1

    new_loc = (x, y)

    if new_loc in TRAPS:
        message = f"""
💀 啊！你踩到了隱藏陷阱！

你的位置：{new_loc}

探險失敗，請重新開始。
"""
        return new_loc, message, draw_map(new_loc, game_over=True), "遊戲結束"

    if new_loc == TREASURE_LOC:
        message = f"""
🎉 恭喜你找到寶藏！

寶藏位置：{TREASURE_LOC}

你成功完成迷霧森林尋寶！
"""
        return new_loc, message, draw_map(new_loc, game_over=True), "遊戲結束"

    distance = calc_distance(new_loc)

    message = f"""
📍 你目前的位置：{new_loc}

📡 探測器顯示，你距離寶藏還有 {round(distance, 2)} 步。

繼續移動，慢慢逼近寶藏。
"""

    return new_loc, message, draw_map(new_loc), ""


with gr.Blocks() as demo:
    gr.Markdown("# 🌲 迷霧森林尋寶")
    gr.Markdown("玩家看不到完整地圖，只能透過距離提示，一步一步找到寶藏。")

    player_state = gr.State(value=START_LOC)

    status = gr.Textbox(label="遊戲狀態", lines=8)
    map_view = gr.HTML(label="地圖")
    game_result = gr.Textbox(label="結果")

    with gr.Row():
        start_btn = gr.Button("重新開始")

    with gr.Row():
        up_btn = gr.Button("⬆️ 上")

    with gr.Row():
        left_btn = gr.Button("⬅️ 左")
        down_btn = gr.Button("⬇️ 下")
        right_btn = gr.Button("➡️ 右")

    start_btn.click(
        fn=start_game,
        inputs=[],
        outputs=[player_state, status, map_view, game_result]
    )

    up_btn.click(
        fn=lambda player_loc: move_player("上", player_loc),
        inputs=[player_state],
        outputs=[player_state, status, map_view, game_result]
    )

    down_btn.click(
        fn=lambda player_loc: move_player("下", player_loc),
        inputs=[player_state],
        outputs=[player_state, status, map_view, game_result]
    )

    left_btn.click(
        fn=lambda player_loc: move_player("左", player_loc),
        inputs=[player_state],
        outputs=[player_state, status, map_view, game_result]
    )

    right_btn.click(
        fn=lambda player_loc: move_player("右", player_loc),
        inputs=[player_state],
        outputs=[player_state, status, map_view, game_result]
    )

demo.launch()