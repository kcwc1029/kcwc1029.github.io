import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

df = pd.read_csv("../Matplotlib_datasets/職訓生活觀察.csv")

# 依日期分組，計算每天總共買了幾杯飲料。
daily_drinks = df.groupby("日期")["飲料杯數"].sum()

plt.figure(figsize=(11, 5))
plt.plot(daily_drinks.index, daily_drinks.values, marker="o", color="#2a9d8f")
plt.title("班上每日飲料杯數變化")
plt.xlabel("日期")
plt.ylabel("飲料杯數")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
