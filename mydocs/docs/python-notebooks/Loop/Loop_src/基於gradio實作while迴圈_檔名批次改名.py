from pathlib import Path
import shutil
import gradio as gr


def batch_rename(files, prefix):
    if not files:
        return "請先上傳檔案！"

    result = []

    # 建立改名後資料夾
    output_dir = Path("renamed_files")
    output_dir.mkdir(exist_ok=True)

    # for：依序處理每個檔案
    for index, file_obj in enumerate(files, start=1):

        old_path = Path(file_obj.name)

        # 新檔名
        new_name = f"{prefix}_{index}{old_path.suffix}"

        new_path = output_dir / new_name

        # 複製並重新命名
        shutil.copy(old_path, new_path)

        result.append(
            f"{old_path.name} → {new_name}"
        )

    return "\n".join(result)


with gr.Blocks() as demo:
    gr.Markdown("# 檔名批次改名工具")
    gr.Markdown(
        "上傳多個檔案後，利用 for 迴圈批次重新命名。"
    )

    file_input = gr.File(
        label="請上傳檔案",
        file_count="multiple"
    )

    prefix_input = gr.Textbox(
        label="請輸入新檔名前綴",
        value="project"
    )

    output = gr.Textbox(
        label="改名結果",
        lines=12
    )

    rename_btn = gr.Button("開始改名")

    rename_btn.click(
        fn=batch_rename,
        inputs=[
            file_input,
            prefix_input
        ],
        outputs=output
    )

demo.launch()