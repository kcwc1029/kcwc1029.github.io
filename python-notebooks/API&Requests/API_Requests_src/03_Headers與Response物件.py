"""認識自訂請求標頭與 Response 物件的重要資訊。"""

import requests

from api_utils import BASE_URL

headers = {
    "Accept": "application/json",
    "User-Agent": "APIRequestsCourse/1.0 (vocational-training)",
    "X-Request-ID": "class-demo-001",
}

response = requests.get(f"{BASE_URL}/products/P065", headers=headers, timeout=5)
response.raise_for_status()

print("請求方法：", response.request.method)
print("請求標頭：", dict(response.request.headers))
print("最終網址：", response.url)
print("回應時間：", response.elapsed.total_seconds(), "秒")
print("回應標頭：", dict(response.headers))
print("商品資料：", response.json()["data"])
