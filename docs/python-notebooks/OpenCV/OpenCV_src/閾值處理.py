import cv2
import numpy as np




# =========================
# 讀取圖片
# =========================

img = cv2.imread("../OpenCV_datasets/white_fish.png")

# =========================
# 轉灰階
# =========================
# 很多影像分析第一步都會轉灰階
#
# 因為：
# - 灰階資料量比較少
# - 不需要考慮顏色
# - 比較容易分析亮度
#
# gray：
# 只剩亮度資訊
gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)


# =========================
# 固定閾值二值化
# =========================
# threshold：
# 用一個固定數值切割圖片
#
# 這裡設定：
# 170
#
# 小於 170：
# → 變黑色(0)
#
# 大於等於 170：
# → 變白色(255)
#
# cv2.THRESH_BINARY：
# 使用黑白二值化模式
#
# "_"：
# 第一個回傳值是 threshold 值
# 這邊不需要，所以用 _
_, fixed = cv2.threshold(
    gray,
    170,
    255,
    cv2.THRESH_BINARY
)


# =========================
# Otsu 自動閾值
# =========================
# Otsu：
# OpenCV 會自動幫你找
# 最適合的切割亮度
#
# 所以這邊 threshold 設 0 即可
#
# 適合：
# - 光線較平均
# - 自動化處理
_, otsu = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)


# =========================
# 自適應閾值
# =========================
# adaptiveThreshold：
# 每個區域使用不同閾值
#
# 適合：
# - 光線不平均
# - 局部太亮或太暗
# - 文件掃描
#
# cv2.ADAPTIVE_THRESH_GAUSSIAN_C：
# 使用高斯加權計算區域亮度
#
# 31：
# 區域大小(block size)
#
# 9：
# 最後再扣掉的數值
adaptive = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    31,
    9
)


# =========================
# 顯示圖片
# =========================

# 原始圖片
cv2.imshow(
    "Original",
    cv2.resize(img, (500, 700))
)

# 灰階圖片
cv2.imshow(
    "Gray",
    cv2.resize(gray, (500, 700))
)

# 固定閾值結果
cv2.imshow(
    "Fixed Threshold",
    cv2.resize(fixed, (500, 700))
)

# Otsu 自動閾值結果
cv2.imshow(
    "Otsu Threshold",
    cv2.resize(otsu, (500, 700))
)

# 自適應閾值結果
cv2.imshow(
    "Adaptive Threshold",
    cv2.resize(adaptive, (500, 700))
)


# =========================
# 等待鍵盤按鍵
# =========================
cv2.waitKey(0)


# =========================
# 關閉所有 OpenCV 視窗
# =========================
cv2.destroyAllWindows()