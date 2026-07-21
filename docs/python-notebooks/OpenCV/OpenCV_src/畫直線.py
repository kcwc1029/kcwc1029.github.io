import cv2
import numpy as np

# 建立空白畫布 (高, 寬, 顏色)
canvas = np.full((500, 500, 3), 255, dtype=np.uint8)

# 畫直線
cv2.line(
    canvas,            # 畫在哪張圖上
    (50, 50),          # 起點
    (450, 450),        # 終點
    (0, 255, 0),       # 顏色(BGR)
    5                  # 線條粗細
)

# 顯示圖片
cv2.imshow("Line", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()