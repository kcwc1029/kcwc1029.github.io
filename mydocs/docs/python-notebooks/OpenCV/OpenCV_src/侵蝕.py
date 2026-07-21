import cv2
import numpy as np

# 讀取圖片
image = cv2.imread("../OpenCV_datasets/Spirited_Away.jpg")

# 檢查圖片是否讀取成功
if image is None:
    print("圖片讀取失敗")
    exit()

# 轉成灰階
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

# 二值化
_, binary = cv2.threshold(
    gray,
    128,
    255,
    cv2.THRESH_BINARY
)

# 建立核心(kernel)
kernel = np.ones((5, 5), np.uint8)

# 侵蝕
erosion = cv2.erode(
    binary,
    kernel,
    iterations=1
)

# 顯示結果
cv2.imshow("Original", image)
# cv2.imshow("Binary", binary)
cv2.imshow("Erosion", erosion)

cv2.waitKey(0)
cv2.destroyAllWindows()