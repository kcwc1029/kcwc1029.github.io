# JSON與資料型態

JSON 是 API 常用的資料交換格式：

```json
{
  "data": [
    {
      "id": "P065",
      "name": "Python入門圖解書",
      "price": 520,
      "free_shipping": true
    }
  ],
  "meta": {
    "page": 1,
    "total": 72
  }
}
```

| JSON         | Python           |
| ------------ | ---------------- |
| object       | `dict`           |
| array        | `list`           |
| string       | `str`            |
| number       | `int` / `float`  |
| true / false | `True` / `False` |
| null         | `None`           |

`data` 通常放主要資料，`meta` 放分頁等描述資訊，但每個 API 的契約可能不同。不能假設全世界都使用同一結構。

## `[]` 與 `.get()` 怎麼選？

必要欄位應用 `[]`：

```python
product_id = item["id"]
# 欄位缺少時立刻拋出 `KeyError`，能及早發現契約改變。
```

真正可選欄位可用 `.get()`：

```python
tag = item.get("tag", "無標籤")
# 所有欄位一律 `.get()`，可能把 API 壞掉偽裝成「資料都是空的」。
```

### 範例：讀取JSONPlaceholder回傳資料，並示範必要欄位驗證

```py
import requests

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(
    url,
    params={"_page": 1, "_limit": 3},
    timeout=5,
)
response.raise_for_status()

payload = response.json()

# JSONPlaceholder 應回傳一個 List。
if not isinstance(payload, list):
    raise ValueError("API 回應不是 List")

print(f"共取得 {len(payload)} 筆資料")

for item in payload:
    # title 與 body 是文章的重要欄位，缺少就視為資料異常。
    if "title" not in item or "body" not in item:
        raise ValueError("API 回應缺少 title 或 body")

    print(
        item["id"],
        item["title"],
        item.get("userId", "未知作者"),
    )
```

## JSON 轉成 DataFrame

```python
df = pd.DataFrame(payload["data"])
df["discount_percent"] = (
    (df["original_price"] - df["price"])
    / df["original_price"]
    * 100
).round(1)
```

Requests 處理網路通訊，pandas 處理資料分析。兩者責任分開，程式比較容易測試。

輸出給 Windows Excel 閱讀：

```python
df.to_csv(output_file, index=False, encoding="utf-8-sig")
```

但不要一收到 JSON 就盲目存檔。先驗證欄位、型態、筆數、唯一性及合理範圍。

```python
"""將 JSONPlaceholder API 資料轉成 DataFrame，整理後輸出 CSV。"""

from pathlib import Path

import pandas as pd
import requests

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(
    url,
    params={"_limit": 30},
    timeout=5,
)
response.raise_for_status()

# JSONPlaceholder 直接回傳 List，不需要使用 ["data"]。
df = pd.DataFrame(response.json())

# 新增衍生欄位。
df["title_length"] = df["title"].str.len()
df["body_length"] = df["body"].str.len()
df["total_length"] = df["title_length"] + df["body_length"]

# 篩選標題與內文較完整的文章。
recommended = df.query(
    "title_length >= 30 and body_length >= 120"
)

# 依總字元數由多到少排序，相同時依文章編號排序。
recommended = recommended.sort_values(
    ["total_length", "id"],
    ascending=[False, True],
)

output_file = OUTPUT_DIR / "JSONPlaceholder文章整理.csv"

recommended.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig",
)

print(
    recommended[
        [
            "id",
            "userId",
            "title",
            "title_length",
            "body_length",
            "total_length",
        ]
    ].to_string(index=False)
)

print("已輸出：", output_file)
```
