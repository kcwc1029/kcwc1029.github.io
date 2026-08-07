"""比較通勤方式的時間分布，辨認中位數、四分位數與離群值。"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chart_utils import DATA_FILE, save_chart, setup_chart

setup_chart()
df = pd.read_csv(DATA_FILE)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(data=df, x="通勤方式", y="每日通勤分鐘", ax=axes[0])
axes[0].set_title("箱型圖：重點摘要清楚")
axes[0].set_xlabel("通勤方式")
axes[0].set_ylabel("每日通勤（分鐘）")

sns.violinplot(data=df, x="通勤方式", y="每日通勤分鐘", inner="quart", ax=axes[1])
axes[1].set_title("小提琴圖：資料密集處較寬")
axes[1].set_xlabel("通勤方式")
axes[1].set_ylabel("每日通勤（分鐘）")
fig.suptitle("不同通勤方式花多少時間？")
save_chart("06_通勤時間箱型圖與小提琴圖.png")
