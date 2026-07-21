"""一次檢查多個數值欄位之間的兩兩關係。"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chart_utils import DATA_FILE, OUTPUT_DIR, setup_chart

setup_chart()
df = pd.read_csv(DATA_FILE)
columns = ["每日睡眠小時", "每日手機小時", "每週自習小時", "課後測驗", "組別"]

grid = sns.pairplot(
    data=df[columns],
    hue="組別",
    diag_kind="hist",
    corner=True,       # 只畫下三角，避免重複並節省空間
    plot_kws={"alpha": 0.7, "s": 45},
)
grid.figure.suptitle("生活習慣與學習成果的兩兩關係", y=1.02)
output = OUTPUT_DIR / "07_多變量關係圖.png"
grid.savefig(output, dpi=150, bbox_inches="tight")
print(f"圖片已輸出：{output}")
plt.show()
