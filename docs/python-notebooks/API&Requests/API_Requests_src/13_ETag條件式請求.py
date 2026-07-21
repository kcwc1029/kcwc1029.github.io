"""用 ETag 避免重複下載沒有改變的 API 資料。"""

import requests

from api_utils import BASE_URL

url = f"{BASE_URL}/products-summary"
first = requests.get(url, timeout=5)
first.raise_for_status()
etag = first.headers["ETag"]
print("第一次：", first.status_code, first.json(), "ETag：", etag)

# 告訴伺服器：若這個版本仍是最新的，不必再傳 body。
second = requests.get(url, headers={"If-None-Match": etag}, timeout=5)
print("第二次：", second.status_code)
if second.status_code == 304:
    print("資料未修改，可以沿用本機快取；回應本文長度：", len(second.content))
else:
    second.raise_for_status()
    print(second.json())
