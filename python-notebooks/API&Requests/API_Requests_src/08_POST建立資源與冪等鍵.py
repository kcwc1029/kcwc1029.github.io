"""POST 建立訂單，並用 Idempotency-Key 防止逾時重送造成重複訂單。"""

import uuid

import requests

from api_utils import BASE_URL

token_response = requests.post(
    f"{BASE_URL}/auth/token",
    json={"username": "student", "password": "python123"},
    timeout=5,
)
token_response.raise_for_status()
token = token_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "Idempotency-Key": str(uuid.uuid4()),
}
order_data = {"items": [{"product_id": "P065", "quantity": 1}]}

first = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers, timeout=5)
first.raise_for_status()
print("第一次狀態碼：", first.status_code)
print("Location：", first.headers.get("Location"))
print("訂單：", first.json())

# 模擬客戶端沒收到第一次回應而重送；相同冪等鍵不會建立第二張訂單。
second = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers, timeout=5)
second.raise_for_status()
print("重送是否沿用原結果：", second.json()["replayed"])
print("兩次訂單 ID 相同：", first.json()["data"]["id"] == second.json()["data"]["id"])
