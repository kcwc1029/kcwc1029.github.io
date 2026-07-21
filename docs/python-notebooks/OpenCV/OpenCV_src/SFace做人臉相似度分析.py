from pathlib import Path

import cv2
import numpy as np


# =========================
# 路徑設定
# =========================

ROOT = Path(__file__).resolve().parents[1]

DATASET_DIR = ROOT / "OpenCV_datasets"

IMAGE_PATH = DATASET_DIR / "豬哥亮.jpg"

YUNET_MODEL = DATASET_DIR / "face_detection_yunet_2023mar.onnx"
SFACE_MODEL = DATASET_DIR / "face_recognition_sface_2021dec.onnx"


# =========================
# 檔案檢查
# =========================

def check_file_exists(file_path, min_size=1):
    if not file_path.exists():
        raise FileNotFoundError(
            f"\n找不到檔案：{file_path.name}\n"
            f"請確認檔案已放到：{DATASET_DIR}\n"
        )

    if file_path.stat().st_size < min_size:
        raise RuntimeError(
            f"\n檔案可能不完整：{file_path.name}\n"
            f"請重新下載後放到：{DATASET_DIR}\n"
        )

    print(f"檔案檢查成功：{file_path.name}")


def read_image_chinese_path(image_path):
    data = np.fromfile(str(image_path), dtype=np.uint8)

    image = cv2.imdecode(
        data,
        cv2.IMREAD_COLOR
    )

    return image


def create_detector(width, height):
    detector = cv2.FaceDetectorYN_create(
        model=str(YUNET_MODEL),
        config="",
        input_size=(width, height),
        score_threshold=0.9,
        nms_threshold=0.3,
        top_k=5000,
    )

    return detector


def create_recognizer():
    recognizer = cv2.FaceRecognizerSF_create(
        model=str(SFACE_MODEL),
        config="",
    )

    return recognizer


def detect_faces(detector, image):
    height, width = image.shape[:2]

    detector.setInputSize(
        (width, height)
    )

    _, faces = detector.detect(image)

    if faces is None:
        return []

    return faces


def get_largest_face(faces):
    if len(faces) == 0:
        return None

    return max(
        faces,
        key=lambda face: face[2] * face[3]
    )


def extract_feature(recognizer, image, face):
    aligned_face = recognizer.alignCrop(
        image,
        face
    )

    feature = recognizer.feature(
        aligned_face
    )

    return feature


def draw_face_box(frame, face, score_text, is_same_person):
    x, y, w, h = face[:4].astype(int)

    if is_same_person:
        color = (0, 255, 0)
        label = "Same Person"
    else:
        color = (0, 0, 255)
        label = "Different Person"

    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        color,
        2
    )

    cv2.putText(
        frame,
        f"{label} | Similarity: {score_text}",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
        cv2.LINE_AA,
    )


def main():

    print("\n" + "=" * 60)
    print("SFace Webcam 人臉相似度比對")
    print("=" * 60)
    print(f"基準照片：{IMAGE_PATH}")
    print(f"YuNet 模型：{YUNET_MODEL}")
    print(f"SFace 模型：{SFACE_MODEL}")
    print("=" * 60 + "\n")

    # =========================
    # 檢查必要檔案
    # =========================

    check_file_exists(
        IMAGE_PATH,
        min_size=1_000
    )

    check_file_exists(
        YUNET_MODEL,
        min_size=100_000
    )

    check_file_exists(
        SFACE_MODEL,
        min_size=30_000_000
    )

    # =========================
    # 讀入基準照片
    # =========================

    reference_image = read_image_chinese_path(
        IMAGE_PATH
    )

    if reference_image is None:
        print(f"讀取圖片失敗：{IMAGE_PATH}")
        return

    ref_height, ref_width = reference_image.shape[:2]

    detector = create_detector(
        ref_width,
        ref_height
    )

    recognizer = create_recognizer()

    reference_faces = detect_faces(
        detector,
        reference_image
    )

    reference_face = get_largest_face(
        reference_faces
    )

    if reference_face is None:
        print("基準照片中沒有偵測到人臉。")
        return

    reference_feature = extract_feature(
        recognizer,
        reference_image,
        reference_face,
    )

    print("\n基準照片人臉特徵建立完成。")
    print("操作說明：")
    print("1. Webcam 對準要比對的人")
    print("2. 綠框代表 Same Person")
    print("3. 紅框代表 Different Person")
    print("4. 按 q 離開程式\n")

    # =========================
    # 開啟 Webcam
    # =========================

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("無法開啟鏡頭。")
        return

    similarity_threshold = 0.363

    while True:

        ret, frame = cap.read()

        if not ret:
            print("無法讀取鏡頭畫面。")
            break

        faces = detect_faces(
            detector,
            frame
        )

        for face in faces:

            current_feature = extract_feature(
                recognizer,
                frame,
                face,
            )

            similarity = recognizer.match(
                reference_feature,
                current_feature,
                cv2.FaceRecognizerSF_FR_COSINE,
            )

            is_same_person = similarity >= similarity_threshold

            draw_face_box(
                frame,
                face,
                score_text=f"{similarity:.3f}",
                is_same_person=is_same_person,
            )

        cv2.putText(
            frame,
            "Press q to quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow(
            "SFace Webcam Face Similarity",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()