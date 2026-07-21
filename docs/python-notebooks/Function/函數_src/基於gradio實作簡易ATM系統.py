import gradio as gr


def show_balance(balance):
    return balance, f"目前餘額：{balance} 元"


def deposit(balance, amount):
    if amount is None or amount <= 0:
        return balance, "存款金額必須大於 0。"

    balance += int(amount)
    return balance, f"成功存入 {int(amount)} 元，目前餘額：{balance} 元"


def withdraw(balance, amount):
    if amount is None or amount <= 0:
        return balance, "提款金額必須大於 0。"

    amount = int(amount)

    if amount > balance:
        return balance, f"餘額不足，無法提款。目前餘額：{balance} 元"

    balance -= amount
    return balance, f"成功提出 {amount} 元，目前餘額：{balance} 元"


def reset_account():
    balance = 1000
    return balance, "ATM 系統已重置，目前餘額：1000 元"


with gr.Blocks() as demo:
    gr.Markdown("# ATM 系統")
    gr.Markdown("可以查詢餘額、存款、提款。預設帳戶餘額為 1000 元。")

    balance_state = gr.State(1000)

    amount_input = gr.Number(
        label="輸入金額",
        precision=0,
        value=100
    )

    with gr.Row():
        balance_btn = gr.Button("查詢餘額")
        deposit_btn = gr.Button("存款", variant="primary")
        withdraw_btn = gr.Button("提款")
        reset_btn = gr.Button("重置帳戶")

    output = gr.Textbox(
        label="系統訊息",
        lines=4,
        interactive=False,
        value="歡迎使用 ATM 系統，目前餘額：1000 元"
    )

    balance_btn.click(
        fn=show_balance,
        inputs=balance_state,
        outputs=[balance_state, output]
    )

    deposit_btn.click(
        fn=deposit,
        inputs=[balance_state, amount_input],
        outputs=[balance_state, output]
    )

    withdraw_btn.click(
        fn=withdraw,
        inputs=[balance_state, amount_input],
        outputs=[balance_state, output]
    )

    reset_btn.click(
        fn=reset_account,
        inputs=[],
        outputs=[balance_state, output]
    )


demo.launch()