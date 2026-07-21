"""使用 catplot 分班比較取得證照者與未取得者的作業完成率。"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chart_utils import DATA_FILE, OUTPUT_DIR, setup_chart

setup_chart()
df = pd.read_csv(DATA_FILE)

grid = sns.catplot(
    data=df,
    x="是否取得證照",
    y="作業完成率",
    col="組別",
    kind="box",
    order=["否", "是"],
    height=4,
)
grid.set_axis_labels("是否取得證照", "作業完成率（%）")
grid.figure.suptitle("作業完成率和證照結果的關係", y=1.05)
output = OUTPUT_DIR / "09_分班證照分析.png"
grid.savefig(output, dpi=150, bbox_inches="tight")
print(f"圖片已輸出：{output}")
plt.show()
