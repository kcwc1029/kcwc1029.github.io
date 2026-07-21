from pathlib import Path
import pickle
import threading

import cv2
import customtkinter as ctk
from tkinter import messagebox


ROOT = Path(__file__).resolve().parents[1]

DATASET_DIR = ROOT / "OpenCV_datasets"

YUNET_MODEL = DATASET_DIR / "face_detection_yunet_2023mar.onnx"
SFACE_MODEL = DATASET_DIR / "face_recognition_sface_2021dec.onnx"

DATABASE_PATH = ROOT / "face_database.pkl"

CAMERA_ID = 0
SCORE_THRESHOLD = 0.9
NMS_THRESHOLD = 0.3
TOP_K = 5000
COSINE_THRESHOLD = 0.363


def check_model_exists(model_path, min_size):
    if not model_path.exists():
        raise FileNotFoundError(
            f"找不到模型：{model_path.name}\n"
            f"請把模型放到：{DATASET_DIR}"
        )

    if model_path.stat().st_size < min_size:
        raise RuntimeError(
            f"模型檔案可能不完整：{model_path.name}\n"
            f"請重新下載後放到：{DATASET_DIR}"
        )


def prepare_models():
    check_model_exists(YUNET_MODEL, 100_000)
    check_model_exists(SFACE_MODEL, 30_000_000)


def create_models(width=640, height=480):
    prepare_models()

    detector = cv2.FaceDetectorYN_create(
        str(YUNET_MODEL),
        "",
        (width, height),
        SCORE_THRESHOLD,
        NMS_THRESHOLD,
        TOP_K
    )

    recognizer = cv2.FaceRecognizerSF_create(
        str(SFACE_MODEL),
        ""
    )

    return detector, recognizer


def load_database():
    if DATABASE_PATH.exists():
        with open(DATABASE_PATH, "rb") as f:
            return pickle.load(f)
    return []


def save_database(database):
    with open(DATABASE_PATH, "wb") as f:
        pickle.dump(database, f)


def get_database_info():
    database = load_database()
    names = [person["name"] for person in database]
    return len(database), names


def update_database_label():
    count, names = get_database_info()

    if count == 0:
        database_label.configure(text="目前尚未註冊任何人臉")
    else:
        show_names = "、".join(names[-6:])
        database_label.configure(
            text=f"目前已註冊 {count} 筆人臉資料：{show_names}"
        )


def clear_database():
    confirm = messagebox.askyesno(
        "確認清除",
        "確定要清除所有已註冊的人臉資料嗎？"
    )

    if not confirm:
        return

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    update_database_label()
    messagebox.showinfo("完成", "已清除所有人臉資料")


def get_largest_face(faces):
    if faces is None:
        return None

    largest_face = None
    largest_area = 0

    for face in faces:
        x, y, w, h = face[:4]
        area = w * h

        if area > largest_area:
            largest_area = area
            largest_face = face

    return largest_face


def recognize_face(feature, database, recognizer):
    best_name = "Unknown"
    best_score = 0

    for person in database:
        score = recognizer.match(
            feature,
            person["feature"],
            cv2.FaceRecognizerSF_FR_COSINE
        )

        if score > best_score:
            best_score = score
            best_name = person["name"]

    if best_score >= COSINE_THRESHOLD:
        return best_name, best_score

    return "Unknown", best_score


def register_face():
    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning("提醒", "請先輸入姓名")
        return

    database = load_database()
    existing_names = [person["name"] for person in database]

    if name in existing_names:
        confirm = messagebox.askyesno(
            "姓名已存在",
            f"{name} 已經註冊過。\n\n是否要再新增一筆同名人臉資料？"
        )

        if not confirm:
            return

    try:
        detector, recognizer = create_models()
    except Exception as e:
        messagebox.showerror("模型錯誤", str(e))
        return

    cap = cv2.VideoCapture(CAMERA_ID)

    if not cap.isOpened():
        messagebox.showerror("錯誤", "無法開啟攝影機")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        height, width = frame.shape[:2]
        detector.setInputSize((width, height))

        _, faces = detector.detect(frame)
        face = get_largest_face(faces)

        if face is not None:
            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"Register: {name}",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Press S to save | Press Q to quit",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
        else:
            cv2.putText(
                frame,
                "No face detected",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            if face is None:
                messagebox.showwarning("提醒", "目前沒有偵測到人臉")
                continue

            aligned_face = recognizer.alignCrop(frame, face)
            feature = recognizer.feature(aligned_face)

            database = load_database()
            database.append({
                "name": name,
                "feature": feature
            })
            save_database(database)

            app.after(0, update_database_label)
            app.after(0, lambda: name_entry.delete(0, "end"))

            messagebox.showinfo("註冊成功", f"{name} 的人臉已註冊完成")
            break

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def start_recognition():
    database = load_database()

    if not database:
        messagebox.showwarning("提醒", "目前沒有人臉資料，請先註冊")
        return

    try:
        detector, recognizer = create_models()
    except Exception as e:
        messagebox.showerror("模型錯誤", str(e))
        return

    cap = cv2.VideoCapture(CAMERA_ID)

    if not cap.isOpened():
        messagebox.showerror("錯誤", "無法開啟攝影機")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        height, width = frame.shape[:2]
        detector.setInputSize((width, height))

        _, faces = detector.detect(frame)

        if faces is not None:
            for face in faces:
                x, y, w, h = face[:4].astype(int)

                aligned_face = recognizer.alignCrop(frame, face)
                feature = recognizer.feature(aligned_face)

                name, score = recognize_face(feature, database, recognizer)

                if name != "Unknown":
                    text = f"{name}, welcome"
                    color = (0, 255, 0)
                else:
                    text = "Unknown"
                    color = (0, 0, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                cv2.putText(
                    frame,
                    f"{text} ({score:.2f})",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2
                )

        cv2.imshow("SFace Recognition System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def run_in_thread(func):
    thread = threading.Thread(target=func, daemon=True)
    thread.start()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SFace 多人人臉辨識系統")
app.geometry("500x430")
app.resizable(False, False)

title_label = ctk.CTkLabel(
    app,
    text="SFace 多人人臉辨識系統",
    font=("Microsoft JhengHei", 26, "bold")
)
title_label.pack(pady=(28, 10))

desc_label = ctk.CTkLabel(
    app,
    text="可連續註冊多位人臉，開始使用後會即時辨識身份",
    font=("Microsoft JhengHei", 14)
)
desc_label.pack(pady=(0, 20))

name_entry = ctk.CTkEntry(
    app,
    width=320,
    height=40,
    placeholder_text="請輸入要註冊的姓名",
    font=("Microsoft JhengHei", 15)
)
name_entry.pack(pady=8)

register_button = ctk.CTkButton(
    app,
    text="註冊人臉(建議輸入英文)",
    width=320,
    height=42,
    font=("Microsoft JhengHei", 16, "bold"),
    command=lambda: run_in_thread(register_face)
)
register_button.pack(pady=8)

start_button = ctk.CTkButton(
    app,
    text="開始使用",
    width=320,
    height=42,
    font=("Microsoft JhengHei", 16, "bold"),
    command=lambda: run_in_thread(start_recognition)
)
start_button.pack(pady=8)

clear_button = ctk.CTkButton(
    app,
    text="清除所有註冊資料",
    width=320,
    height=38,
    fg_color="#8B0000",
    hover_color="#A52A2A",
    font=("Microsoft JhengHei", 14, "bold"),
    command=clear_database
)
clear_button.pack(pady=8)

database_label = ctk.CTkLabel(
    app,
    text="目前尚未註冊任何人臉",
    font=("Microsoft JhengHei", 12),
    wraplength=420
)
database_label.pack(pady=(14, 0))

hint_label = ctk.CTkLabel(
    app,
    text="註冊畫面按 S 儲存｜辨識畫面按 Q 離開",
    font=("Microsoft JhengHei", 12)
)
hint_label.pack(pady=(18, 0))

update_database_label()

app.mainloop()