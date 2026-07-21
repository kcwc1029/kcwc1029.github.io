from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import re

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

data_dir = Path("data")

records = []

for file in data_dir.glob("*年防火宣導成果*.csv"):

    year = int(re.search(r"(\d+)年", file.name).group(1))
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        records.append({
            "年度": year,
            "月份": int(row["類別月份"]),
            "宣導場次": row["合計場次"],
            "宣導人次": row["合計人次"],
            "動員人次": row["合計動員宣導人次"]
        })

data = pd.DataFrame(records)

# 各月累積統計
month_summary = data.groupby("月份", as_index=False).agg({
    "宣導場次": "sum",
    "宣導人次": "sum",
    "動員人次": "sum"
})

month_summary["人次占比"] = (
    month_summary["宣導人次"] / month_summary["宣導人次"].sum() * 100
).round(2)

month_summary = month_summary.sort_values("宣導人次", ascending=False)

print("Q4 各月份宣導人次排序")
print(month_summary)

month_summary.to_csv(
    "Q4_月份宣導旺季分析.csv",
    index=False,
    encoding="utf-8-sig"
)

# -----------------------
# 圖1：年度 × 月份熱圖
# -----------------------

heatmap_data = data.pivot_table(
    index="年度",
    columns="月份",
    values="宣導人次",
    aggfunc="sum"
)

plt.figure(figsize=(12, 6))
plt.imshow(heatmap_data, aspect="auto")

plt.title("年度與月份宣導人次熱圖")
plt.xlabel("月份")
plt.ylabel("年度")

plt.xticks(
    range(len(heatmap_data.columns)),
    heatmap_data.columns
)

plt.yticks(
    range(len(heatmap_data.index)),
    heatmap_data.index
)

plt.colorbar(label="宣導人次")

for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        value = heatmap_data.iloc[i, j]
        plt.text(j, i, int(value), ha="center", va="center", fontsize=8)

plt.tight_layout()
plt.show()

# -----------------------
# 圖2：各月人次占比
# -----------------------

month_order = month_summary.sort_values("月份")

plt.figure(figsize=(10, 5))

plt.bar(
    month_order["月份"],
    month_order["人次占比"]
)

plt.title("各月宣導人次占比")
plt.xlabel("月份")
plt.ylabel("人次占比(%)")

plt.xticks(range(1, 13))
plt.grid(axis="y")

for x, y in zip(month_order["月份"], month_order["人次占比"]):
    plt.text(x, y, f"{y:.1f}%", ha="center", va="bottom")

plt.tight_layout()
plt.show()