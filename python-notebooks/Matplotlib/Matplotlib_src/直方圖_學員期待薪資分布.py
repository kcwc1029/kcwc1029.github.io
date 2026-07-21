import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

df = pd.read_csv("../Matplotlib_datasets/職訓生活觀察.csv")

# 直方圖適合觀察一批數字大多落在哪個範圍。
plt.figure(figsize=(9, 5))
plt.hist(df["期待薪資"], bins=8, color="#e76f51", edgecolor="white")
plt.title("學員期待薪資分布")
plt.xlabel("期待薪資")
plt.ylabel("資料筆數")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
