```python
from pathlib import Path

import qrcode


### 輸出資料夾
current_file = Path(__file__).resolve()  # 取得目前 Python 檔案的絕對路徑
project_root = current_file.parent.parent  # 回到專案根目錄
output_dir = project_root / "Qrcode_outputs"  # QR Code 輸出資料夾

# 若資料夾不存在則自動建立
output_dir.mkdir(parents=True, exist_ok=True)


### QR Code 資料
code_text = "搗蛋鬼別搗蛋"
image_name = "my_qrcode.png"


### 建立 QR Code 物件
# version：
# QR Code 版本，範圍為 1～40
# 數字越大，可儲存的資料越多，但圖片尺寸也會越大
#
# error_correction：
# 容錯等級，用來設定 QR Code 可容忍的損壞程度
# L：約 7%
# M：約 15%
# Q：約 25%
# H：約 30%
#
# box_size：
# 每個小方格（Module）的像素大小
#
# border：
# QR Code 四周留白（Quiet Zone）的寬度
qr = qrcode.QRCode(
    version=10,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,
    border=5,
)


### 加入 QR Code 資料
qr.add_data(code_text)

# fit=True 會依照資料長度，自動調整最適合的版本
qr.make(fit=True)


### 建立 QR Code 圖片
# fill_color：QR Code 顏色
# back_color：背景顏色
qr_image = qr.make_image(

    # 原始風格
    # fill_color="#111111",
    # back_color="#F5F5F5",

    # LINE 風格
    fill_color="#06C755",
    back_color="white",
)

# 轉換成 RGB 格式
qr_image = qr_image.convert("RGB")


### 調整圖片大小
resize_width = 300
resize_height = 300

qr_image = qr_image.resize(
    (resize_width, resize_height)
)


### 儲存 QR Code 圖片
output_file = output_dir / image_name
qr_image.save(output_file)


### 開啟 QR Code 圖片
qr_image.show()


print("QR Code 已產生完成！")
```
