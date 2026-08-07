import pandas as pd

# DataFrame 可以想成 Python 裡的 Excel 表格。
# 每一欄有欄名，每一列是一筆資料。
data = {
    "姓名": ["小安", "小宇", "小婷"],
    "班別": ["Python資料分析班", "網頁前端班", "數位行銷班"],
    "投遞數": [8, 5, 6],
    "面試數": [3, 1, 2],
}

df = pd.DataFrame(data)

print(df)
print("\n資料列數與欄數:", df.shape)
print("\n欄位名稱:", df.columns.tolist())
print("\n前 2 筆:")
print(df.head(2))

