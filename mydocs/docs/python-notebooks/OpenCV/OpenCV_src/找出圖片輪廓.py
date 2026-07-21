import cv2
from pathlib import Path
import numpy as np


### 取得圖片路徑
current_file = Path(__file__).resolve()

image_path = (
    current_file.parent.parent
    / "OpenCV_datasets"
    / "white_fish.png"
)


### 讀取圖片
image = cv2.imdecode(
    np.fromfile(str(image_path), dtype=np.uint8),
    cv2.IMREAD_COLOR
)

if image is None:
    print("圖片讀取失敗")
    raise SystemExit


### 轉成灰階
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)


### Canny 邊緣偵測
edges = cv2.Canny(
    gray,
    100,    # 下限閾值
    200     # 上限閾值
)


### 顯示圖片
cv2.imshow("Original Image", image)
cv2.imshow("Gray Image", gray)
cv2.imshow("Canny Edge", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()