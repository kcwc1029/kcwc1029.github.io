"""用散佈圖探索：自習時間越多，課後成績越高嗎？"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chart_utils import DATA_FILE, save_chart, setup_chart

setup_chart()
df = pd.read_csv(DATA_FILE)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="每週自習小時",
    y="課後測驗",
    hue="組別",                 # 顏色再傳達一個類別資訊
    style="是否取得證照",       # 點的形狀傳達是否取得證照
    size="作業完成率",          # 點的大小傳達作業完成率
    sizes=(40, 180),
    alpha=0.8,
)
plt.title("自習時間、課後成績與證照結果")
plt.xlabel("每週自習（小時）")
plt.ylabel("課後測驗（分）")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
save_chart("自習與成績散佈圖.png")
