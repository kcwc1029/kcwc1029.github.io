"""用直方圖與密度曲線觀察手機使用時間的分布。"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chart_utils import DATA_FILE, save_chart, setup_chart

setup_chart()
df = pd.read_csv(DATA_FILE)

plt.figure(figsize=(10, 5))
# bins 是分成幾個區間；kde=True 會加上平滑的趨勢線。
sns.histplot(data=df, x="每日手機小時", bins=10, kde=True, color="#4C72B0")
plt.axvline(df["每日手機小時"].mean(), color="red", linestyle="--", label="平均值")
plt.title("每天滑手機時間分布")
plt.xlabel("每天使用手機（小時）")
plt.ylabel("人數")
plt.legend()

plt.show()
# save_chart("03_手機時間分布.png")
