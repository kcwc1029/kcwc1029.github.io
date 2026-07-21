

import cv2
import numpy as np



# 讀取圖片
img = cv2.imread("../OpenCV_datasets/white_fish.png")


# =========================
# 高斯模糊
# =========================
# (15, 15) 代表模糊範圍(kernel size)
#
# 數字越大：
# → 模糊越明顯
blur = cv2.GaussianBlur(
    img,
    (15, 15),
    0
)


# =========================
# 縮放方便顯示
# =========================
# img = cv2.resize(img, (500, 700))
# blur = cv2.resize(blur, (500, 700))


# =========================
# 顯示結果
# =========================
cv2.imshow("Original", img)
cv2.imshow("Gaussian Blur", blur)

cv2.waitKey(0)
cv2.destroyAllWindows()