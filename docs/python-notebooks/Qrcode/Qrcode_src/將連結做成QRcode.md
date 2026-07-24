```py
from pathlib import Path

import qrcode
from PIL import Image


### 輸出資料夾
current_file = Path(__file__).resolve()  # 取得目前 Python 檔案的絕對路徑
project_root = current_file.parent.parent  # 回到專案根目錄
output_dir = project_root / "Qrcode_outputs"  # QR Code 輸出資料夾

# 若資料夾不存在則自動建立
output_dir.mkdir(parents=True, exist_ok=True)


### QR Code 資料
code_text = "https://jiashuo.com.tw/new/index.php?mode=&ver=tw&portal=jiashuo"
image_name = "school_qrcode.png"


### 建立 QR Code 圖片
qr_image = qrcode.make(code_text)


### 儲存 QR Code 圖片
output_file = output_dir / image_name
qr_image.save(output_file)


### 開啟 QR Code 圖片
qr_image.show()


print("QR Code 已產生完成！")
```
