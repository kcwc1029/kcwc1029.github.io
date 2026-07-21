# API與Requests

## API 到底是什麼？

API 是 Application Programming Interface，中文常翻成「應用程式介面」。

用餐廳理解 API：餐廳裡：

- 你是 Client。
- 廚房是 Server。
- 菜單是 API 文件。
- 點餐窗口是 Endpoint。
- 點餐動作是 HTTP Method。
- 點餐內容是 Parameters 或 Request Body。
- 號碼牌是 Token。
- 餐點是 Response Body。
- 店員說「售完」是錯誤回應。

你不必進廚房了解每道菜如何製作，只要依菜單規則點餐。API 的價值就是把內部實作藏起來，對外提供穩定的操作方式。

## API 和網頁有什麼不同？

| 項目       | Web API              | 一般網頁                |
| ---------- | -------------------- | ----------------------- |
| 主要使用者 | 程式                 | 人類                    |
| 常見內容   | JSON                 | HTML、CSS、圖片         |
| 結構來源   | API 契約／文件       | 視覺版面                |
| 取得方式   | 依 endpoint 與參數   | 瀏覽器瀏覽              |
| 改版影響   | 版本管理得當時較可控 | HTML class 改名就可能壞 |

因此「API－Requests」與「爬蟲－Requests」雖然都使用 Requests，思考方式不同：

- API 串接：依官方契約交換結構化資料。
- 網頁爬蟲：從面向人類的 HTML 中抽取資料。

API 可以是公開服務、公司內部服務，也可以像本教材只運作於本機。重點不是「上網」，而是兩個軟體元件透過約定介面溝通。

## HTTP Request 與 Response

API 客戶端送出 Request，伺服器傳回 Response：

```text
Python Client                         API Server
     │                                    │
     │ GET /api/v1/products?page=1        │
     │ Accept: application/json           │
     ├───────────────────────────────────>│
     │                                    │ 查詢資料
     │ 200 OK                             │
     │ Content-Type: application/json     │
     │ {"data": [...], "meta": {...}}   │
     │<───────────────────────────────────┤
```

一個 Request 常包含：

- Method：想做什麼。
- URL：對哪個 endpoint 操作。
- Headers：格式、身分與追蹤資訊。
- Query Parameters：搜尋、分頁、排序條件。
- Body：POST、PUT、PATCH 要送出的資料。

一個 Response 常包含：

- Status Code：處理結果。
- Headers：內容格式、快取、版本等資訊。
- Body：JSON 資料或錯誤細節。

### URL 與 endpoint

```text
http://127.0.0.1:8765/api/v1/products?page=2&per_page=10
└協定┘ └────主機────┘└埠┘└───路徑／endpoint──┘└─查詢字串─┘
```

- `/api`：表示 API 路徑。
- `/v1`：第一版 API。
- `/products`：商品資源集合。
- `/products/P065`：單一商品資源。

Endpoint 不只是網址。它通常是 Method 與路徑的組合：

```text
GET  /products       與 POST /products
```

即使路徑相同，方法不同，操作意義也不同。

## REST 與 Resource

REST 是常見的 API 設計風格。初學階段可先抓住兩件事：

1. 把系統資料看成 resource，例如 products、orders、tasks。
2. 用 HTTP Method 表達對 resource 的操作。

| Method | CRUD   | 常見意思 | 範例                     |
| ------ | ------ | -------- | ------------------------ |
| GET    | Read   | 讀取     | 查詢商品                 |
| POST   | Create | 建立     | 建立訂單                 |
| PUT    | Update | 完整取代 | 完整更新任務             |
| PATCH  | Update | 局部修改 | 只把 completed 改成 true |
| DELETE | Delete | 刪除     | 刪除任務                 |

資源路徑通常使用名詞：

```text
推薦：GET /products/P001
不推薦：GET /getProduct?id=P001
```

這是常見設計慣例，不是 HTTP 強制規定。串接既有 API 時，仍以對方文件為準。

### [範例：第一個GET](./API_Requests_src/第一個GET.md)

### Response 不是 dict

`requests.get()` 回傳的是 `Response` 物件，不是 JSON dict。必須呼叫 `.json()` 才會將 Response Body 解析成 Python 物件。

| 屬性／方法                    | 用途                |
| ----------------------------- | ------------------- |
| `response.status_code`        | HTTP 狀態碼         |
| `response.headers`            | 回應標頭            |
| `response.text`               | 解碼後文字          |
| `response.content`            | 原始 bytes          |
| `response.json()`             | JSON 轉 Python 物件 |
| `response.raise_for_status()` | 4xx、5xx 時拋出例外 |
| `response.elapsed`            | 回應時間            |
| `response.request`            | 實際送出的請求      |

重要陷阱：`.json()` 成功只代表 body 是合法 JSON，不代表 API 操作成功。401、404、422、500 也可能回傳 JSON 錯誤，所以仍要檢查狀態碼。

## Query Parameters：查詢、篩選與排序

- [範例：查詢參數與商品搜尋](./API_Requests_src/查詢參數與商品搜尋.md)

Requests 會正確處理 `?`、`&`、空白、中文與特殊符號。不要手動拼接：

```python
# 不建議
url = base_url + "?category=" + category + "&q=" + keyword
```

可以印出 `response.url`，確認最後送出的網址。

本教材商品 API 支援：

| 參數        | 例子      | 意義              |
| ----------- | --------- | ----------------- |
| `page`      | 2         | 第幾頁            |
| `per_page`  | 20        | 每頁筆數，最多 30 |
| `category`  | 學習進修  | 精確篩選分類      |
| `q`         | Python    | 商品名稱關鍵字    |
| `min_price` | 200       | 最低價格          |
| `max_price` | 500       | 最高價格          |
| `sort`      | `-rating` | 評分降冪排序      |

Query Parameter 適合描述「怎樣取得資源」，例如搜尋、排序、分頁。敏感資料不應放 URL，因為網址可能出現在瀏覽紀錄、proxy log 和伺服器 log。

---

## 7. Headers

範例：`API_Requests_src/03_Headers與Response物件.py`

Headers 像包裹外面的標籤，描述資料格式、身分與處理方式：

| Header            | 常見用途               |
| ----------------- | ---------------------- |
| `Accept`          | 客戶端希望收到的格式   |
| `Content-Type`    | Request Body 的格式    |
| `Authorization`   | 認證資訊               |
| `User-Agent`      | 客戶端名稱與版本       |
| `X-Request-ID`    | 跨系統追蹤同一次請求   |
| `Idempotency-Key` | 防止建立操作被重複執行 |
| `If-None-Match`   | 搭配 ETag 做條件式請求 |

```python
headers = {
    "Accept": "application/json",
    "User-Agent": "MyCompanyOrderClient/1.0",
}
response = requests.get(url, headers=headers, timeout=5)
```

HTTP Header 名稱大小寫不敏感，但團隊仍應採一致格式。

---

## 8. JSON 與資料型態

範例：`API_Requests_src/04_JSON巢狀資料與安全取值.py`

JSON 是 API 常用的資料交換格式：

```json
{
  "data": [
    {
      "id": "P065",
      "name": "Python入門圖解書",
      "price": 520,
      "free_shipping": true
    }
  ],
  "meta": {
    "page": 1,
    "total": 72
  }
}
```

| JSON         | Python           |
| ------------ | ---------------- |
| object       | `dict`           |
| array        | `list`           |
| string       | `str`            |
| number       | `int` / `float`  |
| true / false | `True` / `False` |
| null         | `None`           |

`data` 通常放主要資料，`meta` 放分頁等描述資訊，但每個 API 的契約可能不同。不能假設全世界都使用同一結構。

### `[]` 與 `.get()` 怎麼選？

必要欄位應用 `[]`：

```python
product_id = item["id"]
```

欄位缺少時立刻拋出 `KeyError`，能及早發現契約改變。

真正可選欄位可用 `.get()`：

```python
tag = item.get("tag", "無標籤")
```

所有欄位一律 `.get()`，可能把 API 壞掉偽裝成「資料都是空的」。

---

## 9. API 分頁

範例：`API_Requests_src/05_API分頁取得全部資料.py`

伺服器不會一次傳回百萬筆資料，因為：

- 傳輸很慢。
- Client 記憶體壓力大。
- Server 查詢成本高。
- 連線中斷要全部重來。

本 API 回傳：

```json
{
  "data": [],
  "meta": {
    "page": 1,
    "per_page": 15,
    "total": 72,
    "total_pages": 5,
    "has_next": true
  }
}
```

流程：

```text
page=1 → 收 data → has_next?
                   ├─ true → page += 1 → 再請求
                   └─ false → 結束
```

不要只寫固定 `for page in range(1, 6)`，因為資料總數可能改變。也要防止 API 異常造成無限迴圈，正式專案可設定最大頁數並驗證 `total`。

常見分頁還有：

- Offset/limit：`offset=100&limit=20`。
- Cursor：伺服器傳回 `next_cursor`。
- Link Header：下一頁 URL 放在 Header。

Cursor 分頁較能應付資料持續新增，但不能隨意跳到第 100 頁。必須依文件實作。

---

## 10. JSON 轉成 DataFrame

範例：`API_Requests_src/06_API資料轉DataFrame.py`

```python
df = pd.DataFrame(payload["data"])
df["discount_percent"] = (
    (df["original_price"] - df["price"])
    / df["original_price"]
    * 100
).round(1)
```

Requests 處理網路通訊，pandas 處理資料分析。兩者責任分開，程式比較容易測試。

輸出給 Windows Excel 閱讀：

```python
df.to_csv(output_file, index=False, encoding="utf-8-sig")
```

但不要一收到 JSON 就盲目存檔。先驗證欄位、型態、筆數、唯一性及合理範圍。

---

## 11. 狀態碼與錯誤模型

| 狀態碼                    | 意義                | Client 常見處理     |
| ------------------------- | ------------------- | ------------------- |
| 200 OK                    | 成功讀取／更新      | 解析 body           |
| 201 Created               | 成功建立            | 讀資料與 `Location` |
| 204 No Content            | 成功但無 body       | 不可呼叫 `.json()`  |
| 304 Not Modified          | 快取仍有效          | 沿用本機資料        |
| 400 Bad Request           | 參數或 JSON 格式錯  | 修正請求            |
| 401 Unauthorized          | 未認證或 Token 無效 | 更新認證            |
| 403 Forbidden             | 已辨識但沒有權限    | 停止或申請權限      |
| 404 Not Found             | 資源不存在          | 檢查 ID／路徑       |
| 409 Conflict              | 資源狀態衝突        | 重新讀取後處理      |
| 422 Unprocessable Content | 格式合法但驗證失敗  | 修正欄位值          |
| 429 Too Many Requests     | 超過用量            | 尊重 `Retry-After`  |
| 500 Internal Server Error | Server 非預期錯誤   | 記錄、稍後有限重試  |
| 503 Service Unavailable   | 暫時無服務          | 退避後有限重試      |

一致的錯誤 JSON 有助於 Client 處理：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "title 不可空白"
  }
}
```

程式應依穩定的 `code` 判斷，不要只用中文字串比對，因為文案可能修改或翻譯。

---

## 12. Bearer Token 認證

範例：`API_Requests_src/07_Bearer_Token認證.py`

Token 像有期限的電子識別證。Client 先取得 Token，再放入 Header：

```python
headers = {
    "Authorization": f"Bearer {token}"
}
response = requests.get(protected_url, headers=headers, timeout=5)
```

不要：

- 將正式帳密、API Key、Token 寫在原始碼。
- 提交到 Git。
- 印在 log、錯誤截圖或聊天室。
- 放在 Query Parameter。
- 在 HTTP 明文連線傳送正式 Token。

真實專案可從環境變數讀取：

```python
import os

token = os.environ["MY_API_TOKEN"]
```

本教材的 `student / python123` 和 `training-demo-token` 只存在於本機教學 API，沒有外部權限。

### 認證與授權不同

- Authentication：你是誰？
- Authorization：你可以做什麼？

通過登入不代表可以操作所有資源。401 通常偏向未認證，403 通常偏向沒有權限。

---

## 13. POST 與 Request Body

範例：`API_Requests_src/08_POST建立資源與冪等鍵.py`

Requests 的 `json=` 會把 Python dict 序列化成 JSON，並設定適當 `Content-Type`：

```python
order = {
    "items": [
        {"product_id": "P065", "quantity": 1}
    ]
}

response = requests.post(url, json=order, headers=headers, timeout=5)
```

不要混淆：

```python
requests.post(url, json=data)  # application/json
requests.post(url, data=data)  # 通常是表單或原始資料
requests.post(url, files=files)  # multipart/form-data
```

### 201 與 Location

建立成功常回 201，`Location` Header 可以指出新資源位置：

```python
print(response.status_code)
print(response.headers.get("Location"))
```

---

## 14. 冪等性：避免重複訂單

假設 Client 建立訂單後網路中斷：伺服器其實成功了，但 Client 沒收到回應。Client 若直接再 POST 一次，可能產生兩張訂單。

`Idempotency-Key` 像這次操作的唯一號碼：

```python
headers["Idempotency-Key"] = str(uuid.uuid4())
```

同一次商業操作重送時必須使用相同 key，伺服器才知道要回傳原結果；下一張新訂單則要產生新 key。

「產生 key 後立刻每次重送都換新 key」沒有防重效果。正式系統還要規定 key 保存期限、使用者範圍、相同 key 卻不同 body 時的處理方式。

---

## 15. CRUD：POST、GET、PUT、PATCH、DELETE

範例：`API_Requests_src/09_CRUD_POST_PUT_PATCH_DELETE.py`

```text
POST   /tasks      建立
GET    /tasks      讀取
PUT    /tasks/4    完整取代
PATCH  /tasks/4    局部修改
DELETE /tasks/4    刪除
```

### PUT 與 PATCH 的差異

假設原始任務：

```json
{
  "title": "完成作品集",
  "completed": false,
  "priority": "高"
}
```

PUT 通常傳完整狀態：

```json
{
  "title": "完成並發布作品集",
  "completed": true,
  "priority": "中"
}
```

PATCH 只傳要修改的欄位：

```json
{ "completed": true }
```

具體語意仍以 API 文件為準。

### 204 沒有 body

DELETE 成功可能回 204：

```python
response.raise_for_status()
print(response.status_code)
# 不要寫 response.json()，因為沒有 body。
```

---

## 16. Session

範例：`API_Requests_src/10_Session共用設定.py`

`requests.Session()` 可以：

- 共用 Authorization、Accept、User-Agent。
- 保存 Cookie。
- 重用底層連線，減少同一主機反覆連線成本。

```python
with requests.Session() as session:
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })
    response = session.get(url, timeout=5)
```

Session 不是全域變數越大越好。用 `with` 管理生命週期，並注意多執行緒共享 Session 的設計。

---

## 17. timeout 與例外處理

範例：`API_Requests_src/11_錯誤格式與例外處理.py`

網路不是函式直接呼叫，DNS、連線、TLS、Server 與傳輸每一層都可能失敗。

```python
try:
    response = requests.get(url, timeout=(3.05, 10))
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("等待逾時")
except requests.exceptions.ConnectionError:
    print("連線失敗")
except requests.exceptions.HTTPError as error:
    print("HTTP 錯誤", error.response.status_code)
except requests.exceptions.JSONDecodeError:
    print("JSON 格式錯誤")
except requests.exceptions.RequestException as error:
    print("其他 Requests 錯誤", error)
```

`timeout=(3.05, 10)`：

- 第一個數字：connect timeout。
- 第二個數字：read timeout。

read timeout 是等待下一批 bytes 的時間，不是整個工作的絕對總秒數。Requests 預設不會自動 timeout，所以正式程式應明確設定。

### 捕捉順序

具體例外寫前面，父類別 `RequestException` 放最後，否則前面的廣泛捕捉會讓後面永遠不執行。

不要使用：

```python
except:
    pass
```

這會把程式 bug 也吞掉，最後只剩「資料沒有出現」。

---

## 18. 重試與指數退避

範例：`API_Requests_src/12_重試與指數退避.py`

不是每個錯誤都應重試：

- 400：參數錯，重試相同內容仍會錯。
- 401：Token 錯，應更新認證。
- 404：資源不存在，通常不重試。
- 429：依 `Retry-After` 等待。
- 502、503、504：可能是暫時故障，可有限重試。

指數退避會逐漸增加等待時間，避免服務故障時所有 Client 同時狂打 API。

重試 GET 通常比 POST 安全。若 POST 沒有冪等機制，重試可能重複扣款、發信或建立資料。

---

## 19. ETag 與條件式請求

範例：`API_Requests_src/13_ETag條件式請求.py`

ETag 可以想成資料版本指紋：

1. 第一次 GET，Server 回傳資料及 `ETag: "abc123"`。
2. Client 保存資料與 ETag。
3. 下次送 `If-None-Match: "abc123"`。
4. 資料沒變時，Server 回 304，不重傳 body。

這能節省頻寬，但 304 不是錯誤，也通常不能呼叫 `.json()`。

`Cache-Control` 則告訴 Client 快取可以使用多久。認證資料、個資和即時交易資料要特別謹慎，不是所有 API 都適合快取。

---

## 20. 串流下載 API 報表

範例：`API_Requests_src/14_串流下載API報表.py`

大型檔案不應一次塞入記憶體：

```python
with requests.get(url, stream=True, timeout=(3, 30)) as response:
    response.raise_for_status()
    with output_file.open("wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
```

下載前應確認 `Content-Type`、預期大小和檔名。不要直接信任 Server 提供的任意路徑，避免 path traversal。重要檔案還可比對 SHA-256。

---

## 21. API 回應資料驗證

範例：`API_Requests_src/15_API回應資料驗證.py`

HTTP 200 只表示請求層面成功，不代表業務資料一定正確。檢查：

- `data` 是否為 list。
- 必要欄位是否存在。
- ID 是否重複。
- price 是否為正整數。
- rating 是否在 0～5。
- stock 是否為非負整數。
- 實際累計筆數是否符合 `meta.total`。

```python
required = {"id", "name", "price", "rating"}
missing = required - item.keys()
if missing:
    raise ValueError(f"缺少欄位：{missing}")
```

正式專案可使用 Pydantic、JSON Schema 或 OpenAPI 產生的模型進行更完整驗證。

---

## 22. OpenAPI 文件怎麼讀？

串接陌生 API 時，不要只找一段程式碼複製。至少確認：

1. Base URL 與版本。
2. Endpoint 與 Method。
3. Path、Query、Header、Body 參數。
4. 必填、型態、範圍與預設值。
5. 認證方法與權限範圍。
6. 成功狀態碼與 Response Schema。
7. 錯誤格式與錯誤碼。
8. 分頁方式。
9. Rate limit 與 `Retry-After`。
10. 版本、棄用日期與變更紀錄。

OpenAPI 描述的是機器可讀契約；Swagger UI 是常見的互動文件介面。即使有「Try it out」，也不要在正式環境隨便按 POST 或 DELETE。

---

## 23. API 版本管理

本教材路徑包含 `/api/v1`。若未來破壞相容性，可以推出 `/api/v2`，讓舊 Client 有遷移時間。

破壞性改動例如：

- 刪除欄位。
- 改變欄位型態。
- 更改狀態碼語意。
- 將原本可選欄位改為必填。

通常新增可選欄位較容易向後相容，但 Client 也不應假設 JSON 永遠只會有原本那些欄位。

正式 API 應公告 deprecated 狀態與 sunset 日期。Client 要記錄使用版本，不能等 API 關閉當天才處理。

---

## 24. Rate Limit

API 可能限制每分鐘或每日請求數。常見 Header：

```text
RateLimit-Limit: 100
RateLimit-Remaining: 12
RateLimit-Reset: 60
Retry-After: 30
```

實際名稱依 API 文件為準。收到 429 時應：

1. 暫停送出新請求。
2. 尊重 `Retry-After`。
3. 檢查是否能快取或批次取得。
4. 需要時申請合適方案。

不要輪替帳號、Token 或 IP 規避配額。

---

## 25. 安全觀念

### API Key 與 Token

- 放環境變數或祕密管理工具。
- 權限採最小化。
- 定期輪替。
- 外洩時立即撤銷。
- log 中遮蔽。

### TLS

正式 API 應使用 HTTPS。不要為了消除憑證錯誤就寫：

```python
requests.get(url, verify=False)
```

這會關閉伺服器身分驗證。正確做法是修正系統時間、憑證鏈，或使用組織核准的 CA bundle。

### 不可信 URL

若應用程式允許使用者輸入 URL，再由 Server 代為請求，可能造成 SSRF，攻擊者可能探測內網。應建立允許的 scheme、domain、port 與 IP 範圍，不只做字串開頭比對。

### 個資

API 回應中的姓名、電話、地址、健康或財務資料都可能是個資或敏感資訊。只取必要欄位、限制保存期限、加密並控制存取。

---

## 26. 綜合專題：API 商品推薦報表

### 情境

主管希望每天從供應商 API 取得商品，產生高評價平價商品清單。需求：

1. 使用 Session，設定 User-Agent 與 Accept。
2. 每頁 20 筆，抓完所有分頁。
3. 每次請求設定 connect/read timeout。
4. 呼叫 `raise_for_status()`。
5. 驗證總筆數為 API 宣告值，ID 不重複。
6. 計算折扣百分比。
7. 篩選價格不超過 500、評分至少 4.7、庫存大於 0。
8. 依評分降冪、價格升冪排列。
9. 輸出 UTF-8 with BOM CSV。

學生版：

```powershell
uv run python API_Requests_src/16_API商品推薦專題_學生版.py
```

解答版：

```powershell
uv run python API_Requests_src/17_API商品推薦專題_解答.py
```

作品集可以描述：「使用 Requests 串接具分頁的 REST API，加入逾時、狀態檢查、資料契約驗證、Session 與 pandas 報表流程。」不要將教學合成資料描述成真實市場資料。

---

## 27. 課堂練習與答案

### 練習 A：判斷放哪裡

請判斷資料適合放在 Path、Query、Header 還是 Body：

1. 商品 ID `P065`。
2. 第 3 頁。
3. Bearer Token。
4. 建立訂單的商品清單。

答案：Path、Query、Header、Body。

### 練習 B：選擇 Method

1. 查詢商品。
2. 建立任務。
3. 完整改寫任務。
4. 只修改 completed。
5. 刪除任務。

答案：GET、POST、PUT、PATCH、DELETE。

### 練習 C：狀態碼

1. 建立成功通常回什麼？
2. 刪除成功且沒有 body 可回什麼？
3. Token 缺少或無效？
4. 欄位格式合法但業務驗證不通過？
5. 超過 API 配額？

答案：201、204、401、422、429。

### 練習 D：修改搜尋條件

找出手機周邊中，價格不超過 500 元並以價格升冪排序：

```python
params = {
    "category": "手機周邊",
    "max_price": 500,
    "sort": "price",
    "per_page": 30,
}
response = requests.get(f"{BASE_URL}/products", params=params, timeout=5)
```

### 練習 E：找出程式問題

```python
response = requests.get(url)
data = response.json()
```

至少缺少：timeout、狀態碼檢查、例外處理、資料契約驗證。若 URL 由不可信使用者提供，還有 SSRF 風險。

### 加分挑戰

- 在每次請求加入唯一 `X-Request-ID`。
- 計算每頁 `response.elapsed`，找出最慢一頁。
- 將 ETag 與摘要資料保存成本機 JSON 快取。
- 遇到 401 時安全更新 Token，但限制重試次數。
- 為商品回應建立 Pydantic 模型。
- 撰寫自動測試，確認 404 錯誤格式固定。

---

## 28. 常見錯誤與除錯

### `ModuleNotFoundError: No module named 'requests'`

在 `Requests` 資料夾執行：

```powershell
uv sync
```

並確認 VS Code 選擇 `.venv`。

### `ConnectionError` 或 Connection refused

先啟動 `00_啟動本機API伺服器.py`，並保持第一個終端機開啟。

### `JSONDecodeError`

可能收到非 JSON 回應。檢查：

```python
print(response.status_code)
print(response.headers.get("Content-Type"))
print(response.text[:300])
```

正式 log 不要印出 Token、個資或完整敏感 body。

### 401

確認 Authorization 格式：

```text
Authorization: Bearer <token>
```

檢查 Token 是否過期、audience、scope 與系統時間。不要把 Token 直接貼到公開聊天室求助。

### 404

確認 Base URL、版本、endpoint、資源 ID 與結尾斜線規則。

### 422

請求 JSON 可以解析，但欄位缺少、型態或值不符合規則。閱讀錯誤 body，不要只盯著狀態碼。

### 429

尊重 `Retry-After`、降低頻率、使用快取或申請合適配額。

### 204 呼叫 `.json()` 失敗

204 本來就沒有 body。先看狀態碼，不要對每個 Response 無條件 `.json()`。

### 中文 CSV 在 Excel 亂碼

```python
df.to_csv(path, index=False, encoding="utf-8-sig")
```

---

## 29. API 串接交付檢查清單

- [ ] 讀過官方 API 文件與版本說明。
- [ ] Base URL、endpoint、method 正確。
- [ ] Path、Query、Header、Body 放置正確。
- [ ] 所有請求都有 timeout。
- [ ] 4xx、5xx 有明確處理。
- [ ] 錯誤處理不會吞掉程式 bug。
- [ ] 分頁有結束條件並核對總筆數。
- [ ] JSON 必要欄位與型態有驗證。
- [ ] Token 不在程式、Git 或 log。
- [ ] 使用 HTTPS 且未關閉憑證驗證。
- [ ] 有遵守 rate limit 與 `Retry-After`。
- [ ] 重試次數有限且考慮冪等性。
- [ ] POST 交易有防重策略。
- [ ] 204、304 不會錯誤解析 JSON。
- [ ] API 版本與棄用日期有追蹤。
- [ ] 個資只取必要範圍。
- [ ] 輸出放在 `API_Requests_outputs`。

---

## 30. 教學 API 規格速查

| Method | Endpoint            | 認證            | 功能                 |
| ------ | ------------------- | --------------- | -------------------- |
| GET    | `/health`           | 無              | 健康檢查             |
| GET    | `/products`         | 無              | 商品列表、搜尋、分頁 |
| GET    | `/products/{id}`    | 無              | 單一商品             |
| GET    | `/products-summary` | 無              | 支援 ETag 的摘要     |
| GET    | `/products.csv`     | 無              | CSV 報表下載         |
| POST   | `/auth/token`       | 帳密 body       | 取得 Token           |
| GET    | `/tasks`            | Bearer          | 任務列表             |
| POST   | `/tasks`            | Bearer          | 建立任務             |
| PUT    | `/tasks/{id}`       | Bearer          | 完整取代任務         |
| PATCH  | `/tasks/{id}`       | Bearer          | 局部修改任務         |
| DELETE | `/tasks/{id}`       | Bearer          | 刪除任務             |
| POST   | `/orders`           | Bearer + 冪等鍵 | 建立訂單             |
| GET    | `/slow`             | 無              | timeout 教學         |

所有 endpoint 前面都要加：

```text
http://127.0.0.1:8765/api/v1
```

---

## 31. 資料字典

| API 欄位         | CSV 中文欄位 | 型態    | 說明                   |
| ---------------- | ------------ | ------- | ---------------------- |
| `id`             | 商品編號     | string  | P001～P072，唯一識別碼 |
| `name`           | 商品名稱     | string  | 繁體中文生活商品       |
| `category`       | 分類         | string  | 飲料、零食、辦公等     |
| `brand`          | 品牌         | string  | 教學用虛構品牌         |
| `price`          | 價格         | integer | 售價，單位新臺幣       |
| `original_price` | 原價         | integer | 折扣前價格             |
| `rating`         | 評分         | number  | 0～5                   |
| `review_count`   | 評論數       | integer | 合成評論數             |
| `stock`          | 庫存         | integer | 非負整數               |
| `ship_from`      | 出貨地       | string  | 臺灣縣市               |
| `free_shipping`  | 免運         | boolean | JSON true／false       |
| `tag`            | 標籤         | string  | 商品特色               |

---

## 32. 延伸學習

- OpenAPI / Swagger。
- OAuth 2.0 與 OpenID Connect。
- Pydantic 與 JSON Schema。
- FastAPI 建立正式 API。
- pytest 與 API contract testing。
- Webhook 與事件驅動整合。
- 非同步 HTTP Client。
- 資料庫交易、分散式追蹤與可觀測性。

學習新工具時仍要回到核心：API 契約、錯誤處理、安全、資料驗證與可維護性。

---

## 官方參考資料

- [Requests 官方文件](https://requests.readthedocs.io/en/latest/)
- [Requests Quickstart](https://requests.readthedocs.io/en/stable/user/quickstart/)
- [Requests Advanced Usage](https://requests.readthedocs.io/en/stable/user/advanced/)
- [MDN HTTP 狀態碼](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Reference/Status)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

最後請記住：可靠的 API Client 不只是在成功時拿到資料；它還要在逾時、Token 過期、資料改版、服務限流與部分失敗時，能清楚知道發生什麼事並安全停止或恢復。
