"""以帳密取得短期 Token，再呼叫受保護的任務 API。"""

import requests

from api_utils import BASE_URL

# 本機教材帳密；真實密碼不可直接寫在程式碼或提交到 Git。
token_response = requests.post(
    f"{BASE_URL}/auth/token",
    json={"username": "student", "password": "python123"},
    timeout=5,
)
token_response.raise_for_status()
token = token_response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}
tasks_response = requests.get(f"{BASE_URL}/tasks", headers=headers, timeout=5)
tasks_response.raise_for_status()

for task in tasks_response.json()["data"]:
    mark = "完成" if task["completed"] else "待辦"
    print(f'[{mark}] {task["title"]}（優先度：{task["priority"]}）')
