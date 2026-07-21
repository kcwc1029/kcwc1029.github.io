from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import re

# 中文字體
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

data_dir = Path("data")

summary = []

for file in data_dir.glob("*年防火宣導成果*.csv"):

    year = int(re.search(r"(\d+)年", file.name).group(1))

    df = pd.read_csv(file)

    total_events = df["合計場次"].sum()
    total_people = df["合計人次"].sum()
    total_staff = df["合計動員宣導人次"].sum()

    avg_people_per_event = total_people / total_events

    avg_people_per_staff = total_people / total_staff

    summary.append({
        "年度": year,
        "宣導場次": total_events,
        "宣導人次": total_people,
        "動員人次": total_staff,
        "平均每場觸及人數": round(avg_people_per_event, 2),
        "每位動員人員觸及人數": round(avg_people_per_staff, 2)
    })

result = pd.DataFrame(summary)

result = result.sort_values("年度")

print(result)

result.to_csv(
    "Q2_宣導效率分析.csv",
    index=False,
    encoding="utf-8-sig"
)

# -----------------------
# 圖1 平均每場觸及人數
# -----------------------

plt.figure(figsize=(10,5))

plt.plot(
    result["年度"],
    result["平均每場觸及人數"],
    marker="o",
    linewidth=2
)

plt.title("平均每場觸及人數")
plt.xlabel("年度")
plt.ylabel("人數")

plt.grid(True)

for x, y in zip(
    result["年度"],
    result["平均每場觸及人數"]
):
    plt.text(x, y, f"{y:.1f}")

plt.show()


# -----------------------
# 圖2 每位動員人員觸及人數
# -----------------------

plt.figure(figsize=(10,5))

plt.plot(
    result["年度"],
    result["每位動員人員觸及人數"],
    marker="o",
    linewidth=2
)

plt.title("每位動員人員觸及人數")
plt.xlabel("年度")
plt.ylabel("人數")

plt.grid(True)

for x, y in zip(
    result["年度"],
    result["每位動員人員觸及人數"]
):
    plt.text(x, y, f"{y:.1f}")

plt.show()