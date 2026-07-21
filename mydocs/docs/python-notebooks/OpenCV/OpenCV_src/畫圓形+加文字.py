import cv2
import numpy as np

# 建立空白畫布 (高, 寬, 顏色)
canvas = np.full((500, 500, 3), 255, dtype=np.uint8)

# 畫圓形
cv2.circle(
    canvas,
    (250, 200),        # 圓心
    80,                # 半徑
    (0, 0, 255),       # 紅色(BGR)
    3                  # 線條粗細
)

# 加文字
cv2.putText(
    canvas,                     # 要寫字的圖片
    "OpenCV",                   # 顯示的文字內容
    (170, 380),                 # 文字左下角座標 (x, y)
    cv2.FONT_HERSHEY_SIMPLEX,   # 字體樣式
    1.2,                        # 字體大小 (Scale)
    (0, 0, 0),            # 文字顏色 (BGR) → 白色
    2                           # 文字粗細
)

# 顯示圖片
cv2.imshow("Circle + Text", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()