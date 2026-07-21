import cv2

# 讀取圖片
image = cv2.imread("../OpenCV_datasets/white_fish.png")

# 轉灰階
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

# 邊緣偵測
edges = cv2.Canny(
    gray,
    100,
    200
)

# 顯示結果
cv2.imshow("Original", image)
cv2.imshow("Edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()