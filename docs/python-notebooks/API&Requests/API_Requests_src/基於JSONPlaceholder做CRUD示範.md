```text
POST   /tasks      建立
POST   /posts      建立文章
GET    /posts/1    讀取文章
PUT    /posts/1    完整更新
PATCH  /posts/1    局部更新
DELETE /posts/1    刪除文章
```

```python
"""JSONPlaceholder CRUD 示範。"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# -------------------------
# GET
# -------------------------
print("=== GET ===")

response = requests.get(f"{BASE_URL}/posts/1")
response.raise_for_status()

print(response.json())

# -------------------------
# POST
# -------------------------
print("\n=== POST ===")

new_post = {
    "title": "Python API 教學",
    "body": "使用 requests 建立文章。",
    "userId": 1,
}

response = requests.post(
    f"{BASE_URL}/posts",
    json=new_post,
)
response.raise_for_status()

print(response.status_code)
print(response.json())

# -------------------------
# PUT
# -------------------------
print("\n=== PUT ===")

updated_post = {
    "id": 1,
    "title": "新的標題",
    "body": "新的內容",
    "userId": 1,
}

response = requests.put(
    f"{BASE_URL}/posts/1",
    json=updated_post,
)
response.raise_for_status()

print(response.json())

# -------------------------
# PATCH
# -------------------------
print("\n=== PATCH ===")

response = requests.patch(
    f"{BASE_URL}/posts/1",
    json={
        "title": "只修改標題",
    },
)
response.raise_for_status()

print(response.json())

# -------------------------
# DELETE
# -------------------------
print("\n=== DELETE ===")

response = requests.delete(
    f"{BASE_URL}/posts/1",
)
response.raise_for_status()

print("HTTP Status:", response.status_code)
```
