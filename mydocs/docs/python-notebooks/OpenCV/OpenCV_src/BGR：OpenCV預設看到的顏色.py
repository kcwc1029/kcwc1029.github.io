### 範例程式：讀取圖片並查看 BGR 像素
import cv2

# OpenCV 讀進來的圖片，預設就是 BGR
image = cv2.imread("../OpenCV_datasets/white_fish.png")

# 檢查圖片是否讀取成功
if image is None:
    print("圖片讀取失敗，請檢查路徑或檔名")
else:
    # 取得左上角像素
    pixel = image[0, 0]

    print("左上角像素 BGR 數值：", pixel)

    # 顯示圖片
    cv2.imshow("BGR Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()