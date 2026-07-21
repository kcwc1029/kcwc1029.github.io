import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

df = pd.read_csv("../Matplotlib_datasets/職訓生活觀察.csv")

output_dir = Path("../Matplotlib_outputs")

summary = df.groupby("學員姓名").agg(
    平均學習時數=("學習時數", "mean"),
    平均作業分數=("作業分數", "mean"),
    總投遞履歷數=("投遞履歷數", "sum"),
    總面試邀約數=("面試邀約數", "sum"),
)

# 輸出整理後的 CSV，之後可以給 Excel 或主管報表使用。
summary.to_csv(output_dir / "學員學習求職摘要.csv", encoding="utf-8-sig")

plt.figure(figsize=(10, 5))
plt.bar(summary.index, summary["平均作業分數"], color="#264653")
plt.title("各學員平均作業分數")
plt.xlabel("學員")
plt.ylabel("平均作業分數")
plt.ylim(60, 105)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

# dpi 代表圖片解析度，數字越高通常越清楚，檔案也會比較大。
plt.savefig(output_dir / "各學員平均作業分數.png", dpi=150)
plt.show()

print(f"已輸出：{output_dir / '學員學習求職摘要.csv'}")
print(f"已輸出：{output_dir / '各學員平均作業分數.png'}")
