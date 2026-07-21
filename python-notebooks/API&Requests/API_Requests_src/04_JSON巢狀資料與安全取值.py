"""讀取 JSON 的 data/meta 結構，並示範必要欄位驗證。"""

import requests

from api_utils import BASE_URL

response = requests.get(f"{BASE_URL}/products", params={"page": 1, "per_page": 3}, timeout=5)
response.raise_for_status()
payload = response.json()

# data 與 meta 是本 API 契約的必要欄位，缺少時應直接發現問題。
if "data" not in payload or "meta" not in payload:
    raise ValueError("API 回應缺少 data 或 meta")

meta = payload["meta"]
print(f'目前第 {meta["page"]} 頁，共 {meta["total_pages"]} 頁、{meta["total"]} 筆')

for item in payload["data"]:
    # tag 是非關鍵顯示資訊，可用 get 提供合理預設值。
    print(item["id"], item["name"], item.get("tag", "無標籤"))
