"""分別處理逾時、連線、HTTP 與 JSON 格式錯誤。"""

import requests

from api_utils import BASE_URL


def call_api(url: str, params: dict | None = None) -> dict | None:
    try:
        response = requests.get(url, params=params, timeout=(2, 1))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("逾時：API 在期限內沒有傳回資料")
    except requests.exceptions.ConnectionError:
        print("連線失敗：請檢查網址、網路與伺服器")
    except requests.exceptions.HTTPError as error:
        response = error.response
        try:
            detail = response.json().get("error", {})
        except requests.exceptions.JSONDecodeError:
            detail = {"message": "伺服器未回傳標準 JSON 錯誤"}
        print(f'HTTP {response.status_code}：{detail.get("code", "UNKNOWN")}－{detail.get("message")}')
    except requests.exceptions.JSONDecodeError:
        print("JSON 解析失敗：回應格式可能不符合 API 契約")
    except requests.exceptions.RequestException as error:
        print("其他 Requests 錯誤：", error)
    return None


call_api(f"{BASE_URL}/products/不存在")
call_api(f"{BASE_URL}/products", {"page": "不是數字"})
call_api(f"{BASE_URL}/slow", {"seconds": 3})
