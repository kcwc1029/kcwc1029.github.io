import gradio as gr


menu = {
    "漢堡": 60,
    "薯條": 35,
    "可樂": 25,
    "雞塊": 45,
    "蛋餅": 40
}


def calculate_total(orders):
    total = 0
    for item in orders:
        total += menu[item]
    return total


def format_orders(orders):
    if not orders:
        return "目前沒有點任何餐點。"

    text = "=== 已點餐點 ===\n"
    for item in orders:
        text += f"{item}: {menu[item]} 元\n"

    text += f"\n目前總金額：{calculate_total(orders)} 元"
    return text


def add_order(item, orders):
    if orders is None:
        orders = []

    orders.append(item)
    order_text = format_orders(orders)

    return orders, order_text


def clear_orders():
    orders = []
    return orders, "目前沒有點任何餐點。", ""


def checkout(orders):
    if not orders:
        return "沒有點任何餐點。"

    receipt = "=== 收據 ===\n"

    for item in orders:
        receipt += f"{item}: {menu[item]} 元\n"

    total = calculate_total(orders)
    receipt += f"\n總金額：{total} 元"

    return receipt


with gr.Blocks() as demo:
    gr.Markdown("# 點餐系統")
    gr.Markdown("選擇餐點後按下「加入餐點」，最後按「結帳」產生收據。")

    orders_state = gr.State([])

    menu_text = "=== 菜單 ===\n"
    for item, price in menu.items():
        menu_text += f"{item}: {price} 元\n"

    gr.Textbox(
        value=menu_text,
        label="菜單",
        lines=7,
        interactive=False
    )

    food_dropdown = gr.Dropdown(
        choices=list(menu.keys()),
        value="漢堡",
        label="選擇餐點"
    )

    with gr.Row():
        add_btn = gr.Button("加入餐點", variant="primary")
        checkout_btn = gr.Button("結帳")
        clear_btn = gr.Button("清空訂單")

    order_output = gr.Textbox(
        label="目前訂單",
        lines=8,
        interactive=False
    )

    receipt_output = gr.Textbox(
        label="收據",
        lines=8,
        interactive=False
    )

    add_btn.click(
        fn=add_order,
        inputs=[food_dropdown, orders_state],
        outputs=[orders_state, order_output]
    )

    checkout_btn.click(
        fn=checkout,
        inputs=orders_state,
        outputs=receipt_output
    )

    clear_btn.click(
        fn=clear_orders,
        inputs=[],
        outputs=[orders_state, order_output, receipt_output]
    )


demo.launch()