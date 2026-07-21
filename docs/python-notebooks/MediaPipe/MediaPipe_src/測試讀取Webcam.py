# file_name: opencv_webcam_basic.py

import cv2


# 開啟 Webcam
cap = cv2.VideoCapture(0)


# 檢查攝影機是否成功開啟
if not cap.isOpened():
    print("無法開啟攝影機")
    exit()


print("按下 q 可以離開程式")


while True:

    # 讀取 Webcam 畫面
    success, frame = cap.read()

    # 如果讀取失敗
    if not success:
        print("讀取畫面失敗")
        break


    # 顯示畫面
    cv2.imshow("OpenCV Webcam", frame)


    # 按 q 離開
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# 釋放 Webcam
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()