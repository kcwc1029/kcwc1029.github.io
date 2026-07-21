import cv2
import mediapipe as mp


# 初始化 MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def main():

    # 開啟 Webcam
    cap = cv2.VideoCapture(0)

    # 建立人臉偵測模型
    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.5
    ) as face_detection:

        while cap.isOpened():

            # 讀取畫面
            success, frame = cap.read()

            # 如果讀取失敗
            if not success:
                print("讀不到 Webcam 畫面")
                break


            # 左右翻轉
            frame = cv2.flip(frame, 1)

            # BGR 轉 RGB
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # 人臉偵測
            results = face_detection.process(rgb_frame)


            # 預設人數
            face_count = 0


            # 如果有偵測到人臉
            if results.detections:

                # 計算人數
                face_count = len(results.detections)

                # 繪製每張人臉框
                for detection in results.detections:
                    mp_drawing.draw_detection(
                        frame,
                        detection
                    )


            # 顯示目前人數
            cv2.putText(
                frame,
                f"Students Count: {face_count}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


            # 顯示畫面
            cv2.imshow(
                "AI Classroom Attendance Counter",
                frame
            )


            # 按 q 離開
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    # 釋放資源
    cap.release()

    # 關閉視窗
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()