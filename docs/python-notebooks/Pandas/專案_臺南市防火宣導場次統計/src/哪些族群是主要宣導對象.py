from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import re

# 中文字體設定
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

data_dir = Path("data")

records = []

for file in data_dir.glob("*年防火宣導成果*.csv"):

    year = int(re.search(r"(\d+)年", file.name).group(1))
    df = pd.read_csv(file)

    # 找出所有族群欄位：例如「學校場次」對應「學校人次」
    for col in df.columns:

        if col.endswith("場次") and col != "合計場次":

            group_name = col.replace("場次", "")
            people_col = group_name + "人次"

            if people_col in df.columns:

                total_events = df[col].sum()
                total_people = df[people_col].sum()

                records.append({
                    "年度": year,
                    "族群": group_name,
                    "場次": total_events,
                    "人次": total_people
                })

# 整理成 DataFrame
data = pd.DataFrame(records)

# 各族群跨年度累積
group_summary = data.groupby("族群", as_index=False).agg({
    "場次": "sum",
    "人次": "sum"
})

# 計算占比
group_summary["場次占比"] = group_summary["場次"] / group_summary["場次"].sum() * 100
group_summary["人次占比"] = group_summary["人次"] / group_summary["人次"].sum() * 100

# 排序：以累積人次由高到低
group_summary = group_summary.sort_values("人次", ascending=False)

# 四捨五入
group_summary["場次占比"] = group_summary["場次占比"].round(2)
group_summary["人次占比"] = group_summary["人次占比"].round(2)

print("Q3 各族群累積宣導成果")
print(group_summary)

# 輸出 CSV
group_summary.to_csv(
    "Q3_主要宣導對象分析.csv",
    index=False,
    encoding="utf-8-sig"
)


# -----------------------
# 圖1：各族群累積人次
# -----------------------

plt.figure(figsize=(12, 6))

plt.bar(
    group_summary["族群"],
    group_summary["人次"]
)

plt.title("各族群累積宣導人次")
plt.xlabel("族群")
plt.ylabel("累積宣導人次")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y")

plt.tight_layout()
plt.show()


# -----------------------
# 圖2：各族群累積場次
# -----------------------

group_by_events = group_summary.sort_values("場次", ascending=False)

plt.figure(figsize=(12, 6))

plt.bar(
    group_by_events["族群"],
    group_by_events["場次"]
)

plt.title("各族群累積宣導場次")
plt.xlabel("族群")
plt.ylabel("累積宣導場次")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y")

plt.tight_layout()
plt.show()


# -----------------------
# 圖3：人次占比圓餅圖
# -----------------------

top_groups = group_summary.head(6).copy()
other_people = group_summary.iloc[6:]["人次"].sum()

pie_data = pd.concat([
    top_groups[["族群", "人次"]],
    pd.DataFrame([{"族群": "其他", "人次": other_people}])
])

plt.figure(figsize=(8, 8))

plt.pie(
    pie_data["人次"],
    labels=pie_data["族群"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("主要宣導對象人次占比")
plt.show()