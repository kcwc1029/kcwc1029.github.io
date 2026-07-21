import gradio as gr


def generate_colors(step):
    html = ""

    step = int(step)

    # 防止 step 太小造成爆量生成
    if step <= 0:
        return "step 必須大於 0"

    # for：批次生成 RGB 顏色
    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):

                color = f"rgb({r}, {g}, {b})"

                html += f"""
                <div style="
                    width:120px;
                    height:120px;
                    background:{color};
                    border-radius:12px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-weight:bold;
                    box-shadow:0 4px 10px rgba(0,0,0,0.2);
                ">
                    {r}<br>{g}<br>{b}
                </div>
                """

    # 外層容器
    html = f"""
    <div style="
        display:flex;
        flex-wrap:wrap;
        gap:12px;
    ">
        {html}
    </div>
    """

    return html


with gr.Blocks() as demo:
    gr.Markdown("# RGB 顏色產生器")
    gr.Markdown(
        "利用 for 迴圈，自動產生大量 RGB 色塊。"
    )

    step_slider = gr.Slider(
        minimum=32,
        maximum=128,
        step=1,
        value=64,
        label="RGB 間隔(step)"
    )

    output = gr.HTML()

    generate_btn = gr.Button("產生色塊")

    generate_btn.click(
        fn=generate_colors,
        inputs=step_slider,
        outputs=output
    )

demo.launch()