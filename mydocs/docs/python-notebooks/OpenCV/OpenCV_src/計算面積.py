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


### 計算每個輪廓面積
for index, contour in enumerate(contours, start=1):

    # 面積
    area = cv2.contourArea(contour)

    print(f"物件{index} 面積：{area:.0f}")

    # 取得中心點
    M = cv2.moments(contour)

    if M["m00"] != 0:

        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])

        # 畫輪廓
        cv2.drawContours(
            result,
            [contour],
            -1,
            (0, 255, 0),
            2
        )

        # 顯示面積
        cv2.putText(
            result,
            f"{area:.0f}",
            (center_x - 30, center_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )


### 顯示總數
cv2.putText(
    result,
    f"Count : {len(contours)}",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 0, 0),
    2
)


### 顯示圖片
cv2.imshow("Original", image)
# cv2.imshow("Binary", binary)
cv2.imshow("Area Detection", result)

cv2.waitKey(0)
cv2.destroyAllWindows()