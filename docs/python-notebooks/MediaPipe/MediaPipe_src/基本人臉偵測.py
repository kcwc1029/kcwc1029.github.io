import cv2
import mediapipe as mp


# 載入 MediaPipe 人臉偵測模組
mp_face_detection = mp.solutions.face_detection

# 載入繪圖工具，用來畫出人臉框與關鍵資訊
mp_drawing = mp.solutions.drawing_utils


def main():

    # 開啟預設攝影機
    # 0 代表第一台攝影機
    cap = cv2.VideoCapture(0)

    # 建立人臉偵測器
    with mp_face_detection.FaceDetection(

        # model_selection=0
        # 適合 2 公尺內近距離人臉
        # 1 則適合較遠距離人臉
        model_selection=0,

        # 最低信心值
        # 偵測結果必須高於 60% 才會被保留
        min_detection_confidence=0.6,

    ) as face_detection:

        # 持續讀取攝影機畫面
        while cap.isOpened():

            # 讀取一張影像
            success, frame = cap.read()

            # 如果讀取失敗就離開
            if not success:
                print("讀不到 Webcam 畫面")
                break

            # 左右翻轉
            # 讓畫面看起來像照鏡子
            frame = cv2.flip(frame, 1)

            # OpenCV 使用 BGR
            # MediaPipe 使用 RGB
            # 因此要先轉換色彩格式
            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # 執行人臉偵測
            results = face_detection.process(rgb)

            # 如果有偵測到人臉
            if results.detections:

                # 逐一處理每張臉
                for detection in results.detections:

                    # 繪製人臉框與信心值
                    mp_drawing.draw_detection(
                        frame,
                        detection
                    )

            # 顯示結果畫面
            cv2.imshow(
                "AI Face Detection - Press q to quit",
                frame
            )

            # 按 q 離開程式
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # 釋放攝影機資源
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()


# 程式進入點
if __name__ == "__main__":
    main()