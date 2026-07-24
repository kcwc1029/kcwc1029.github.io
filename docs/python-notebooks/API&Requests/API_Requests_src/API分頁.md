伺服器不會一次傳回百萬筆資料，因為：

- 傳輸很慢。
- Client 記憶體壓力大。
- Server 查詢成本高。
- 連線中斷要全部重來。

本 API 回傳流程：

```text
page=1 → 收 data → has_next?
                   ├─ true → page += 1 → 再請求
                   └─ false → 結束
```

不要只寫固定 `for page in range(1, 6)`，因為資料總數可能改變。也要防止 API 異常造成無限迴圈，正式專案可設定最大頁數並驗證 `total`。

常見分頁還有：

- Offset/limit：`offset=100&limit=20`。
- Cursor：伺服器傳回 `next_cursor`。
- Link Header：下一頁 URL 放在 Header。

Cursor 分頁較能應付資料持續新增，但不能隨意跳到第 100 頁。必須依文件實作。

```py
"""使用 JSONPlaceholder 分頁取得全部文章資料。"""

import time
import requests

page = 1
all_posts = []

while True:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={
            "_page": page,
            "_limit": 15,
        },
        timeout=(3.05, 10),
    )
    response.raise_for_status()

    posts = response.json()

    # 沒有資料代表已到最後一頁
    if not posts:
        break

    all_posts.extend(posts)

    print(f"第 {page} 頁取得 {len(posts)} 筆，累計 {len(all_posts)} 筆")

    page += 1
    time.sleep(0.1)

print("API 宣告總筆數：", response.headers.get("X-Total-Count"))
print("實際取得總筆數：", len(all_posts))
```
