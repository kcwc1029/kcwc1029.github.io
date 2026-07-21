import customtkinter as ctk
from PIL import Image
import requests

### 下載網路圖片並轉成 CTkImage
def download_image(url, size):
    from io import BytesIO
    response = requests.get(url) # 下載圖片
    image_data = BytesIO(response.content) # 轉成 PIL Image
    pil_image = Image.open(image_data)

    # 建立 CTkImage
    ctk_image = ctk.CTkImage(
        light_image=pil_image,
        dark_image=pil_image,
        size=size
    )
    return ctk_image


def main():
    ### GUI
    app = ctk.CTk()
    app.geometry("400x300")

    ### 使用函數下載圖片
    cat_image = download_image(
        "https://i.pinimg.com/1200x/41/e2/5f/41e25f50ab9c59bc18df85de4176d5b1.jpg",
        (150, 150)
    )

    ### 顯示圖片
    image_label = ctk.CTkLabel(
        app,
        image=cat_image,
        text=""
    )

    image_label.pack(pady=30)
    app.mainloop()  # 啟動 GUI


if __name__ == "__main__":
    main()