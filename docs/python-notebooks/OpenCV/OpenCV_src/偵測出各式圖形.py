from pathlib import Path

import cv2
import numpy as np


# 取得專案根目錄
ROOT = Path(__file__).resolve().parents[1]

# 圖片路徑
image_path = ROOT / "OpenCV_datasets" / "contours_shapes.png"


# 使用 imdecode + fromfile
# 避開 Windows 中文路徑問題
img = cv2.imdecode(
    np.fromfile(str(image_path), dtype=np.uint8),
    cv2.IMREAD_COLOR
)


# 檢查圖片是否成功讀取
if img is None:
    raise FileNotFoundError(f"讀不到圖片：{image_path}")


# 轉灰階
gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)


# 二值化
_, binary = cv2.threshold(
    gray,
    230,
    255,
    cv2.THRESH_BINARY_INV
)


# 找輪廓
contours, _ = cv2.findContours(
    binary,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


# 複製原圖，用來畫輪廓
vis = img.copy()


# 畫出所有輪廓
cv2.drawContours(
    vis,
    contours,
    -1,
    (0, 0, 255),
    3
)


# 印出輪廓數量
print("contours:", len(contours))


# =========================
# 縮放圖片
# =========================
resize_original = cv2.resize(img, (500, 700))
resize_binary = cv2.resize(binary, (500, 700))
resize_vis = cv2.resize(vis, (500, 700))


# =========================
# 顯示圖片
# =========================
cv2.imshow("Original", resize_original)
cv2.imshow("Binary", resize_binary)
cv2.imshow("Contours", resize_vis)


# 等待按鍵
cv2.waitKey(0)


# 關閉所有視窗
cv2.destroyAllWindows()