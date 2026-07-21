import cv2
import numpy as np

# 建立白底
image = np.full((400, 400, 3), 255, dtype=np.uint8)

# 畫黑色矩形
cv2.rectangle(
    image,
    (100, 100),
    (300, 300),
    (0, 0, 0),
    -1
)

# 灰階
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

# 二值化
_, binary = cv2.threshold(
    gray,
    127,
    255,
    cv2.THRESH_BINARY_INV
)

# 找輪廓
contours, hierarchy = cv2.findContours(
    binary,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# 畫輪廓
cv2.drawContours(
    image,
    contours,
    -1,
    (0, 0, 255),
    3
)

cv2.imshow("Binary", binary)
cv2.imshow("Contour", image)

cv2.waitKey(0)
cv2.destroyAllWindows()