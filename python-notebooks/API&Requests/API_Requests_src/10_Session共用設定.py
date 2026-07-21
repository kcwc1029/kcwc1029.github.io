"""用 Session 共用 Token、Headers 並重用連線。"""

import requests

from api_utils import BASE_URL

with requests.Session() as session:
    token_response = session.post(
        f"{BASE_URL}/auth/token",
        json={"username": "student", "password": "python123"},
        timeout=5,
    )
    token_response.raise_for_status()

    session.headers.update({
        "Authorization": f'Bearer {token_response.json()["access_token"]}',
        "Accept": "application/json",
        "User-Agent": "APIRequestsCourse/1.0",
    })

    # 後續請求自動帶上共用標頭。
    tasks = session.get(f"{BASE_URL}/tasks", timeout=5)
    tasks.raise_for_status()
    print("任務數：", tasks.json()["meta"]["total"])
    print("實際送出的 Authorization：", tasks.request.headers["Authorization"])
