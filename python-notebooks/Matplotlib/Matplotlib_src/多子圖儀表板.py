import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

df = pd.read_csv("../Matplotlib_datasets/職訓生活觀察.csv")

weekly = df.groupby("週次").agg(
    平均學習時數=("學習時數", "mean"),
    平均作業分數=("作業分數", "mean"),
    總投遞履歷數=("投遞履歷數", "sum"),
    總面試邀約數=("面試邀約數", "sum"),
)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(weekly.index, weekly["平均學習時數"], marker="o", color="#2a9d8f")
axes[0, 0].set_title("每週平均學習時數")
axes[0, 0].set_xlabel("週次")
axes[0, 0].set_ylabel("小時")

axes[0, 1].plot(weekly.index, weekly["平均作業分數"], marker="o", color="#f4a261")
axes[0, 1].set_title("每週平均作業分數")
axes[0, 1].set_xlabel("週次")
axes[0, 1].set_ylabel("分數")

axes[1, 0].bar(weekly.index, weekly["總投遞履歷數"], color="#457b9d")
axes[1, 0].set_title("每週總投遞履歷數")
axes[1, 0].set_xlabel("週次")
axes[1, 0].set_ylabel("投遞數")

axes[1, 1].bar(weekly.index, weekly["總面試邀約數"], color="#e76f51")
axes[1, 1].set_title("每週總面試邀約數")
axes[1, 1].set_xlabel("週次")
axes[1, 1].set_ylabel("邀約數")

for ax in axes.flat:
    ax.grid(True, alpha=0.25)

fig.suptitle("職訓班學習與求職追蹤儀表板", fontsize=16)
plt.tight_layout()
plt.show()
