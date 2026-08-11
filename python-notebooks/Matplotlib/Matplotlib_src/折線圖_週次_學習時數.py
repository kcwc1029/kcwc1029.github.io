import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

# x 軸通常放「時間、順序、分類」。
weeks = [1, 2, 3, 4, 5, 6]

# y 軸通常放「數值」。
study_hours = [12, 15, 18, 22, 24, 28]

plt.figure(figsize=(8, 5))
plt.plot(weeks, study_hours, marker="o", linewidth=2)

# 圖表不是只有線，標題與座標軸文字會幫讀者理解這張圖在說什麼。
plt.title("職訓班每週平均學習時數")
plt.xlabel("週次")
plt.ylabel("平均學習時數")
plt.grid(True, alpha=0.3)

plt.show()
