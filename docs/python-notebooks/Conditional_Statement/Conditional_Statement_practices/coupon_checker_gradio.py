import gradio as gr


def check_coupon(order_price, is_member, coupon_limit):
    ### 從這裡開始寫


description = """
# Problem. 電商優惠券判斷

* 購物金額(order_price)為 2500。
* 是否為會員(is_member)為 True。
* 優惠券最低門檻(coupon_limit)為 2000。

接著，如果：
* 購物金額達到門檻且為會員，則輸出：「優惠券套用成功」
* 否則輸出「無法使用優惠券」

"""


with gr.Blocks() as demo:
    gr.Markdown(description)

    order_price_input = gr.Number(
        label="購物金額",
        value=2500,
        precision=0
    )

    member_input = gr.Checkbox(
        label="是否為會員",
        value=True
    )

    coupon_limit_input = gr.Number(
        label="優惠券最低門檻",
        value=2000,
        precision=0
    )

    check_button = gr.Button("檢查優惠券")

    result_output = gr.Textbox(
        label="檢查結果"
    )

    check_button.click(
        fn=check_coupon,
        inputs=[
            order_price_input,
            member_input,
            coupon_limit_input
        ],
        outputs=result_output
    )


demo.launch()