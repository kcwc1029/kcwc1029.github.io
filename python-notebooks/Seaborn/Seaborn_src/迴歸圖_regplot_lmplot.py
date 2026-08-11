"""加入迴歸線，描述自習時間和成績的整體關係。"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../Seaborn_datasets/職訓生活與學習紀錄.csv")

# lmplot 是圖形層級函式，可直接依 col 拆成多張小圖。
grid = sns.lmplot(
    data=df,
    x="每週自習小時",
    y="課後測驗",
    col="組別",
    hue="組別",
    height=4,
    aspect=0.9,
    ci=95,
    scatter_kws={"alpha": 0.7},
)
grid.set_axis_labels("每週自習（小時）", "課後測驗（分）")
grid.figure.suptitle("各班自習時間與成績趨勢", y=1.05)

plt.show()
