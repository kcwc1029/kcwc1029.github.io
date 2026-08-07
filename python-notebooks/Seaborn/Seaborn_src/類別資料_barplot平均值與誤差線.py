"""barplot 範例：比較各班平均課後測驗成績。"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from chart_utils import DATA_FILE, save_chart, setup_chart

# 套用 Seaborn 主題、中文字型及輸出資料夾設定。
setup_chart()

# 讀取 72 筆職訓學員資料。
df = pd.read_csv(DATA_FILE)

# 先用 pandas 算出各班平均值，方便核對圖表。
class_mean = (
    df.groupby("組別", as_index=False)["課後測驗"]
    .mean()
    .sort_values("課後測驗", ascending=False)
)
print("各班平均課後測驗成績：")
print(class_mean.to_string(index=False))

# 建立兩張並排的圖，展示有無誤差線的差別。
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# 左圖：關閉誤差線，課程初期可先專注比較平均值。
left_chart = sns.barplot(
    data=df,
    x="組別",
    y="課後測驗",
    estimator="mean",       # 每根柱子的高度代表該班平均值
    errorbar=None,           # 不顯示誤差線
    hue="組別",
    palette="Set2",
    legend=False,
    ax=axes[0],
)
axes[0].set_title("不顯示誤差線：專注比較平均值")
axes[0].set_xlabel("班別")
axes[0].set_ylabel("平均課後測驗（分）")
axes[0].set_ylim(0, 100)

# 在每根柱子上方顯示平均分數。
for container in left_chart.containers:
    left_chart.bar_label(container, fmt="%.1f", padding=3)

# 右圖：顯示 95% 信賴區間，呈現平均值估計的不確定程度。
sns.barplot(
    data=df,
    x="組別",
    y="課後測驗",
    estimator="mean",
    errorbar=("ci", 95),
    capsize=0.15,            # 誤差線兩端橫線的寬度
    hue="組別",
    palette="Set2",
    legend=False,
    ax=axes[1],
)
axes[1].set_title("顯示 95% 信賴區間：呈現不確定性")
axes[1].set_xlabel("班別")
axes[1].set_ylabel("平均課後測驗（分）")
axes[1].set_ylim(0, 100)

fig.suptitle("各班平均課後測驗成績", fontsize=18)
save_chart("barplot平均值與誤差線.png")
