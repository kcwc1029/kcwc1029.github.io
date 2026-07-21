import cv2
import numpy as np

# 建立空白畫布 (高, 寬, 顏色)
canvas = np.full((500, 500, 3), 255, dtype=np.uint8)

# 畫矩形
cv2.rectangle(
    canvas,
    (100, 100),        # 左上角
    (400, 300),        # 右下角
    (255, 0, 0),       # 藍色(BGR)
    3                  # 邊框粗細
)

# 顯示圖片
cv2.imshow("Rectangle", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()