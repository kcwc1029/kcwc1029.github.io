# file_name: 02_face_detection_online_status.py

import cv2
import mediapipe as mp


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def main():

    # 開啟 Webcam
    cap = cv2.VideoCapture(0)

    # 建立 Face Detection 模型
    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.6,
    ) as face_detection:

        while cap.isOpened():

            # 讀取 Webcam 畫面
            success, frame = cap.read()

            # 如果讀取失敗
            if not success:
                print("讀不到 Webcam 畫面")
                break


            # 左右翻轉畫面
            frame = cv2.flip(frame, 1)

            # BGR 轉 RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 進行人臉偵測
            results = face_detection.process(rgb)


            # 預設狀態
            status_text = "Waiting..."
            status_color = (0, 0, 255)


            # 如果有偵測到人臉
            if results.detections:

                status_text = "Student Online"
                status_color = (0, 255, 0)

                # 繪製人臉框
                for detection in results.detections:
                    mp_drawing.draw_detection(frame, detection)


            # 顯示狀態文字
            cv2.putText(
                frame,
                status_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                status_color,
                2
            )


            # 顯示畫面
            cv2.imshow(
                "AI Face Detection - Press q to quit",
                frame
            )


            # 按 q 離開
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    # 釋放資源
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()