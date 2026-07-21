from pathlib import Path
import qrcode
from PIL import Image


# 要編碼的文字
code_text = "搗蛋鬼別導彈"


# 建立 QRCode
qr = qrcode.QRCode(
    version=10,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,
    border=5
)

qr.add_data(code_text)

# 自動調整大小
qr.make(fit=True)


# 生成 QRCode 圖片
img = qr.make_image(
    fill_color="#222222",
    back_color="#FFFFFF"
)

# 轉成 RGB
img = img.convert("RGB")


# 讀取 Logo 圖片
BASE_DIR = Path(__file__).resolve().parent.parent
logo_path = BASE_DIR / "Qrcode_datasets" / "小貓拿花花.jpg"
logo = Image.open(logo_path)
logo = logo.convert("RGB")

# 取得大小
img_width, img_height = img.size
logo_width, logo_height = logo.size


# 調整 Logo 大小
logo_size = (
    int(img_width * 0.25),
    int(img_height * 0.25)
)

logo = logo.resize(
    logo_size,
    Image.Resampling.LANCZOS
)



# 計算置中位置
logo_width, logo_height = logo.size

position = (
    (img_width - logo_width) // 2,
    (img_height - logo_height) // 2
)

img.paste(logo, position) # 貼上 Logo


# 儲存圖片
# output_path = Path("cat_qrcode.png")
# img.save(output_path)
# print(f"QRCode 已儲存：{output_path.resolve()}")

img.show() # 顯示圖片