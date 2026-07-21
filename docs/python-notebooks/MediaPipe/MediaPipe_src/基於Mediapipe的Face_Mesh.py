import cv2
import mediapipe as mp


# 載入 MediaPipe Face Mesh 模組
# 用來偵測人臉上的 468 個關鍵點
mp_face_mesh = mp.solutions.face_mesh

# 載入繪圖工具
# 用來將偵測結果畫到畫面上
mp_drawing = mp.solutions.drawing_utils


# 建立繪圖樣式
# thickness：線條粗細
# circle_radius：關鍵點大小
# color：BGR 顏色格式
drawing_spec = mp_drawing.DrawingSpec(
    thickness=1,
    circle_radius=1,
    color=(0, 255, 0)
)


def main():

    # 開啟預設攝影機
    # 0 代表第一台 Webcam
    cap = cv2.VideoCapture(0)

    # 建立 Face Mesh 模型
    with mp_face_mesh.FaceMesh(

        # 最多同時偵測幾張臉
        max_num_faces=1,

        # 啟用精細模式
        # 可額外偵測眼睛與嘴唇細節
        refine_landmarks=True,

        # 人臉偵測最低信心值
        min_detection_confidence=0.5,

        # 人臉追蹤最低信心值
        min_tracking_confidence=0.5

    ) as face_mesh:

        # 持續讀取攝影機畫面
        while cap.isOpened():

            # 讀取一張影像
            success, frame = cap.read()

            # 如果讀取失敗就離開
            if not success:
                print("讀不到 Webcam 畫面")
                break

            # 左右翻轉畫面
            # 讓使用者看起來像照鏡子
            frame = cv2.flip(frame, 1)

            # OpenCV 使用 BGR
            # MediaPipe 使用 RGB
            # 因此需要先轉換格式
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # 執行 Face Mesh 分析
            # 找出人臉上的 468 個特徵點
            results = face_mesh.process(rgb_frame)

            # 如果畫面中有偵測到人臉
            if results.multi_face_landmarks:

                # 逐一處理每張臉
                for face_landmarks in results.multi_face_landmarks:

                    # 將人臉網格畫到畫面上
                    # FACEMESH_TESSELATION 會畫出完整三角網格
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec
                    )

            # 顯示結果畫面
            cv2.imshow(
                "Face Mesh Visualizer",
                frame
            )

            # 按 q 鍵結束程式
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # 釋放攝影機資源
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()


# 程式進入點
if __name__ == "__main__":
    main()