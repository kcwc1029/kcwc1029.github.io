from pathlib import Path
import qrcode
from PIL import Image


# vCard 個人資料
vc_str = """BEGIN:VCARD
VERSION:3.0
FN;CHARSET=UTF-8:陳維誠 Wei-Cheng Chen
TEL;CELL:+886-979-956-XXX
ORG;CHARSET=UTF-8:伽碩XXXXX公司
TITLE;CHARSET=UTF-8:可憐的社畜狗狗
EMAIL:n96144250@gs.ncku.edu.tw
URL:https://XXXXXX.github.io/
ADR;CHARSET=UTF-8:台南市東區大學路1號
END:VCARD
"""

# 建立 QRCode
qr = qrcode.QRCode(
    version=10,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,
    border=5
)

qr.add_data(vc_str.encode("utf-8"))
qr.make(fit=True)

# 生成圖片
img = qr.make_image(
    fill_color="#222222",
    back_color="#FFFFFF"
)

img = img.convert("RGB")

# 儲存圖片
# output_path = Path("個資Qrcode.png")
# img.save(output_path)
# print(f"QRCode 已儲存：{output_path.resolve()}")

img.show() # 顯示圖片