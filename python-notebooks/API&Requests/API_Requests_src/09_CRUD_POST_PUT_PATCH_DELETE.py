"""完整演示建立、讀取、取代、局部修改與刪除任務。"""

import requests

from api_utils import BASE_URL

token_response = requests.post(f"{BASE_URL}/auth/token", json={"username": "student", "password": "python123"}, timeout=5)
token_response.raise_for_status()
headers = {"Authorization": f'Bearer {token_response.json()["access_token"]}'}

# Create：建立新任務。
created = requests.post(f"{BASE_URL}/tasks", json={"title": "完成 API 作品集", "priority": "高"}, headers=headers, timeout=5)
created.raise_for_status()
task_id = created.json()["data"]["id"]
print("POST 建立：", created.json()["data"])

# Read：讀取任務清單。
tasks = requests.get(f"{BASE_URL}/tasks", headers=headers, timeout=5)
tasks.raise_for_status()
print("GET 任務總數：", tasks.json()["meta"]["total"])

# PUT：完整取代，因此三個可編輯欄位都要提供。
replaced = requests.put(f"{BASE_URL}/tasks/{task_id}", json={"title": "完成並發布 API 作品集", "completed": False, "priority": "中"}, headers=headers, timeout=5)
replaced.raise_for_status()
print("PUT 取代：", replaced.json()["data"])

# PATCH：只修改指定欄位。
patched = requests.patch(f"{BASE_URL}/tasks/{task_id}", json={"completed": True}, headers=headers, timeout=5)
patched.raise_for_status()
print("PATCH 局部修改：", patched.json()["data"])

# DELETE 成功回傳 204，沒有 JSON body，不可呼叫 response.json()。
deleted = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers, timeout=5)
deleted.raise_for_status()
print("DELETE 狀態碼：", deleted.status_code, "回應本文長度：", len(deleted.content))
