"""驗證 API 筆數、唯一性、型別與合理範圍。"""

import requests

from api_utils import BASE_URL

response = requests.get(f"{BASE_URL}/products", params={"per_page": 30}, timeout=5)
response.raise_for_status()
payload = response.json()
items = payload["data"]

assert isinstance(items, list), "data 應該是 list"
assert payload["meta"]["total"] >= len(items), "總筆數不可小於本頁筆數"
assert len({item["id"] for item in items}) == len(items), "本頁商品 ID 重複"

required_fields = {"id", "name", "price", "rating", "stock"}
for index, item in enumerate(items, start=1):
    missing = required_fields - item.keys()
    assert not missing, f"第 {index} 筆缺少欄位：{missing}"
    assert isinstance(item["price"], int) and item["price"] > 0, "價格必須是正整數"
    assert 0 <= item["rating"] <= 5, "評分必須介於 0～5"
    assert isinstance(item["stock"], int) and item["stock"] >= 0, "庫存必須是非負整數"

print(f"驗證通過：本頁 {len(items)} 筆，API 總筆數 {payload['meta']['total']} 筆")
