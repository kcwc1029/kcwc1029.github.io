import gradio as gr


# 初始餘額
balance = 5000


def atm_withdraw(money):
    global balance

    money = int(money)

    while money > balance:
        return (
            f"提款失敗！\n"
            f"你的餘額只有 {balance} 元。\n"
            f"請重新輸入較小金額。"
        )

    balance -= money

    return (
        f"提款成功！\n"
        f"你領了 {money} 元。\n"
        f"剩餘餘額：{balance} 元"
    )


demo = gr.Interface(
    fn=atm_withdraw,
    inputs=gr.Number(label="請輸入提款金額"),
    outputs=gr.Textbox(label="ATM 結果"),
    title="ATM 提款機",
    description="如果提款金額超過餘額，系統會要求重新輸入。"
)

demo.launch()