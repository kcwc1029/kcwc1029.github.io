from pathlib import Path

import cv2
import numpy as np


# =========================
# 取得專案根目錄
# =========================
ROOT = Path(__file__).resolve().parents[1]


# =========================
# 圖片路徑
# =========================
image_path = ROOT / "OpenCV_datasets" / "contours_shapes.png"


# =========================
# 使用 imdecode 避開 Windows 中文路徑問題
# =========================
img = cv2.imdecode(
    np.fromfile(str(image_path), dtype=np.uint8),
    cv2.IMREAD_COLOR
)


# =========================
# 檢查圖片是否成功讀取
# =========================
if img is None:
    raise FileNotFoundError(f"讀不到圖片：{image_path}")


# =========================
# 轉灰階
# =========================
gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)


# =========================
# 二值化
# =========================
# 白色背景 → 黑色
# 黑色圖形 → 白色
#
# 方便後續找輪廓
_, binary = cv2.threshold(
    gray,
    230,
    255,
    cv2.THRESH_BINARY_INV
)


# =========================
# 尋找輪廓
# =========================
contours, _ = cv2.findContours(
    binary,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


# =========================
# 逐個輪廓分析
# =========================
for c in contours:

    # 計算輪廓面積
    area = cv2.contourArea(c)

    # 過濾太小雜訊
    if area < 500:
        continue

    # 計算輪廓周長
    peri = cv2.arcLength(c, True)

    # 多邊形近似
    #
    # 用較少點數
    # 近似原本輪廓
    approx = cv2.approxPolyDP(
        c,
        0.03 * peri,
        True
    )

    # 建立外接矩形
    x, y, w, h = cv2.boundingRect(approx)

    # =========================
    # 判斷形狀
    # =========================
    #
    # 幾個角
    # 大致代表幾邊形
    #
    # triangle → 3邊
    # rectangle → 4邊
    # pentagon → 5邊
    # 其他 → circle
    if len(approx) == 3:
        name = "triangle"

    elif len(approx) == 4:
        name = "rectangle"

    elif len(approx) == 5:
        name = "pentagon"

    else:
        name = "circle"

    # =========================
    # 畫外接矩形
    # =========================
    cv2.rectangle(
        img,
        (x, y),
        (x + w, y + h),
        (0, 0, 255),
        2
    )

    # =========================
    # 顯示形狀名稱
    # =========================
    cv2.putText(
        img,
        name,
        (x, y - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )


# =========================
# 縮放圖片
# =========================
resize_binary = cv2.resize(binary, (500, 700))
resize_img = cv2.resize(img, (500, 700))


# =========================
# 顯示結果
# =========================
cv2.imshow("Binary", resize_binary)
cv2.imshow("Shape Detection", resize_img)


# =========================
# 等待按鍵
# =========================
cv2.waitKey(0)


# =========================
# 關閉所有 OpenCV 視窗
# =========================
cv2.destroyAllWindows()