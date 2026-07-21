# 如果你需要更精準地控制 QR Code 的外觀，可以使用 qrcode.QRCode() 方法

# 建立 QR Code 物件，並設定參數
# qr = qrcode.QRCode(
#     version=5, # QR Code 的版本，從 1 到 40。版本數字越大，可以儲存的資料越多
#     error_correction=qrcode.constants.ERROR_CORRECT_M, # 容錯等級，用來設定 QR Code 的損壞容忍度。
#     box_size=10, # 每個小方塊（模塊）的像素大小
#     border=4 # QR Code 周圍的邊界寬度。
# )

from pathlib import Path
import qrcode
from PIL import Image

# 定義要編碼的文字內容
code_text = "搗蛋鬼別搗蛋"

# 建立 QR Code 物件
qr = qrcode.QRCode(
    version=10,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,   # 每個小方格大小
    border=5       # 外框大小
)

qr.add_data(code_text) # 加入資料
qr.make(fit=True) # 自動調整大小


# 建立 QRCode 圖片
img = qr.make_image(
    # 原始版
    # fill_color="#111111",
    # back_color="#F5F5F5"
    
    # LINE 風格
    fill_color="#06C755",
    back_color="white"    
)

img = img.convert("RGB")


# 調整圖片大小
img_resized = img.resize((300, 300))


# 儲存圖片
# output_path = Path("my_qrcode.png")
# img_resized.save(output_path)
# print(f"QRCode 已儲存：{output_path.resolve()}")


# 開啟圖片
img_resized.show()