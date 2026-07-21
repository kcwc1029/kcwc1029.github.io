import cv2
import numpy as np
from pathlib import Path


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


### 轉灰階
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)


### 不同 Canny 閾值
edge_1 = cv2.Canny(gray, 30, 100)
edge_2 = cv2.Canny(gray, 100, 200)
edge_3 = cv2.Canny(gray, 200, 300)


### 在圖片上加標題
cv2.putText(
    edge_1,
    "30,100",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    255,
    2
)

cv2.putText(
    edge_2,
    "100,200",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    255,
    2
)

cv2.putText(
    edge_3,
    "200,300",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    255,
    2
)


### 三張圖片水平拼接
result = cv2.hconcat([
    edge_1,
    edge_2,
    edge_3
])


### 顯示結果
cv2.imshow("Canny Threshold Comparison", result)

cv2.waitKey(0)
cv2.destroyAllWindows()