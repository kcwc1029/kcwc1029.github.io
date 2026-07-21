import cv2

# 讀取圖片
image = cv2.imread("../OpenCV_datasets/white_fish.png")

# 轉成灰階圖片
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 顯示原圖
cv2.imshow("Original Image", image)

# 顯示灰階圖片
cv2.imshow("Gray Image", gray_image)

# 等待使用者按任意鍵
cv2.waitKey(0)

# 關閉所有視窗
cv2.destroyAllWindows()