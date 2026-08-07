"""計算相關係數並用 heatmap 找出值得深入調查的關係。"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chart_utils import DATA_FILE, save_chart, setup_chart

setup_chart()
df = pd.read_csv(DATA_FILE)
columns = ["每日通勤分鐘", "每日睡眠小時", "每日手機小時", "每週自習小時", "課前測驗", "課後測驗", "作業完成率"]
correlation = df[columns].corr()
print(correlation.round(2))

plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation,
    annot=True,        # 把數字寫進格子
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    square=True,
)
plt.title("生活習慣與學習成果相關係數")
save_chart("08_相關係數熱圖.png")
