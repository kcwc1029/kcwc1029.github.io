"""對暫時性 GET 錯誤設定有限次重試與指數退避。"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api_utils import BASE_URL

retry = Retry(
    total=3,
    connect=3,
    read=3,
    status=3,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET", "HEAD"),
    respect_retry_after_header=True,
)

with requests.Session() as session:
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = session.get(f"{BASE_URL}/health", timeout=(3, 10))
    response.raise_for_status()
    print(response.json())
