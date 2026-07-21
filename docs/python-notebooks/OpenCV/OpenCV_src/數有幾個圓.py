import cv2
import numpy as np
from pathlib import Path


### 圖片路徑
current_file = Path(__file__).resolve()


image_path = (
    current_file.parent.parent
    / "OpenCV_datasets"
    / "coin.jpg"
)

### 讀取圖片
image = cv2.imdecode(
    np.fromfile(str(image_path), dtype=np.uint8),
    cv2.IMREAD_COLOR
)

if image is None:
    print("圖片讀取失敗")
    raise SystemExit


### 轉灰階
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)


### 二值化
_, binary = cv2.threshold(
    gray,
    127,
    255,
    cv2.THRESH_BINARY
)


### 找輪廓
contours, hierarchy = cv2.findContours(
    binary,
    cv2.RETR_EXTERNAL,      # 只找最外層輪廓
    cv2.CHAIN_APPROX_SIMPLE
)


### 複製圖片
result = image.copy()


### 畫出輪廓
cv2.drawContours(
    result,
    contours,
    -1,
    (0, 255, 0),
    3
)


### 計算數量
count = len(contours)

print(f"找到 {count} 個物件")


### 顯示數量
cv2.putText(
    result,
    f"Count : {count}",
    (20, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)


### 顯示圖片
cv2.imshow("Original", image)
cv2.imshow("Binary", binary)
cv2.imshow("Contours", result)

cv2.waitKey(0)
cv2.destroyAllWindows()