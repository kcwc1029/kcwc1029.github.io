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
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


### 複製圖片
result = image.copy()


### 計算每個物件中心點
for index, contour in enumerate(contours, start=1):

    # 計算 Moments
    M = cv2.moments(contour)

    if M["m00"] == 0:
        continue

    # 中心點座標
    center_x = int(M["m10"] / M["m00"])
    center_y = int(M["m01"] / M["m00"])

    print(
        f"物件{index} 中心點：({center_x}, {center_y})"
    )

    # 畫輪廓
    cv2.drawContours(
        result,
        [contour],
        -1,
        (0, 255, 0),
        2
    )

    # 畫中心十字
    cv2.drawMarker(
        result,
        (center_x, center_y),
        (0, 0, 255),
        markerType=cv2.MARKER_CROSS,
        markerSize=25,
        thickness=2
    )

    # 顯示座標
    cv2.putText(
        result,
        f"({center_x},{center_y})",
        (center_x + 10, center_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2
    )


### 顯示圖片
cv2.imshow("Original", image)
# cv2.imshow("Binary", binary)
cv2.imshow("Center Point", result)

cv2.waitKey(0)
cv2.destroyAllWindows()