import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

df = pd.read_csv("../Matplotlib_datasets/職訓生活觀察.csv")

# 圓餅圖適合看「整體裡面各部分的比例」。
drink_counts = df.groupby("飲料類別")["飲料杯數"].sum().sort_values(ascending=False)

plt.figure(figsize=(7, 7))
plt.pie(
    drink_counts.values,
    labels=drink_counts.index,
    autopct="%.1f%%",
    startangle=90,
)
plt.title("班上飲料偏好比例")
plt.tight_layout()
plt.show()
