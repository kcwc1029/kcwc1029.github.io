

import cv2
import numpy as np


# =========================
# 讀取圖片
# =========================
img = cv2.imread("../OpenCV_datasets/white_fish.png")

# =========================
# 銳化 kernel
# =========================
# 中間像素加強
# 周圍像素扣掉一些
#
# 最後效果：
# 邊緣更明顯
kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])


# =========================
# 套用銳化
# =========================
sharp = cv2.filter2D(
    img,
    -1,
    kernel
)


# =========================
# 縮放方便顯示
# =========================
# img = cv2.resize(img, (500, 700))
# sharp = cv2.resize(sharp, (500, 700))


# =========================
# 顯示結果
# =========================
cv2.imshow("Original", img)
cv2.imshow("Sharpen", sharp)

cv2.waitKey(0)
cv2.destroyAllWindows()