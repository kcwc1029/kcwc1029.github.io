import cv2
import numpy as np
from pathlib import Path


### 取得圖片路徑
current_file = Path(__file__).resolve()

image_path = (
    current_file.parent.parent
    / "OpenCV_datasets"
    / "Jacky_Wu.jpg"
)


### 讀取圖片
image = cv2.imdecode(
    np.fromfile(str(image_path), dtype=np.uint8),
    cv2.IMREAD_COLOR
)

if image is None:
    print("圖片讀取失敗，請確認圖片路徑與檔名")
    print(image_path)
    raise SystemExit


### 縮放圖片，避免視窗太大
image = cv2.resize(image, (500, 500))


### 轉灰階
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


### 模糊處理
# 先把雜訊柔化，Canny 才不會抓到太多亂線
blur = cv2.GaussianBlur(
    gray,
    (5, 5),
    0
)


### Canny 邊緣偵測
edges = cv2.Canny(
    blur,
    50,
    150
)


### 反相處理
# 原本是黑底白線，反相後會變成白底黑線，比較像素描線稿
sketch = cv2.bitwise_not(edges)


### 顯示結果
cv2.imshow("Original", image)
cv2.imshow("Gray", gray)
cv2.imshow("Canny Edge", edges)
cv2.imshow("Sketch Style", sketch)

cv2.waitKey(0)
cv2.destroyAllWindows()