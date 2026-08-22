# Selenium 爬蟲：從動態網頁到 BeautifulSoup

## 先決定是否需要 Selenium

三條爬蟲路線

### 路線 A：Requests + JSON

若 JavaScript 只是呼叫 API 取得 JSON，通常直接使用 API 更快、更省記憶體，也較容易檢查欄位。但「在 Network 看得到」不等於自動獲得使用授權；仍要確認服務條款、驗證方式、資料授權和頻率限制。

```python
response = requests.get("https://example.com/api/jobs", timeout=10)
response.raise_for_status()
data = response.json()
```

### 路線 B：Requests + BeautifulSoup

適合資料直接存在網站回傳的 HTML：新聞列表、文章內文、Wikipedia、HTML 表格、排行榜、一般分頁、標題、作者、日期、價格與連結。

```python
import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://example.com/news",
    headers={"User-Agent": "TrainingCrawler/1.0"},
    timeout=10,
)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")
news_list = soup.select(".news-item")
```

### 路線 C：Selenium

適合必須完成瀏覽器行為後資料才出現：

- 點擊「載入更多」或無限捲動。
- 切換頁籤、選擇縣市或日期後才載入。
- 點開對話框後才顯示。
- 經一般登入流程才能看，而且自動化被明確允許。
- 頁面內容必須執行 JavaScript 才建立。
- Requests 回傳 HTML 裡沒有目標資料，也沒有合適的可用 API。

Selenium 真的啟動瀏覽器，因此慢、耗記憶體，並容易受動畫、彈窗與載入時序影響。它是必要時使用的工具，不是預設答案。

## 2. 實際判斷三步驟

### 第一步：查看原始碼

在瀏覽器按 `Ctrl+U`，再用 `Ctrl+F` 搜尋畫面上的職缺或商品名稱。找到通常表示 Requests 可取得。找不到只是一個線索，不代表一定要 Selenium。

「檢查元素」顯示的是 JavaScript 執行後的目前 DOM；「檢視原始碼」接近伺服器最初送回的 HTML。兩者可能完全不同。

### 第二步：Python 直接驗證

```python
response = requests.get(url, timeout=10)
response.raise_for_status()
keyword = "Python 工程師"
print("原始 HTML 有資料" if keyword in response.text else "請繼續檢查 Network")
```

除了文字，也要確認不是登入頁或錯誤頁。

### 第三步：Network

開啟 `F12 → Network → Fetch/XHR → 重新整理`，觀察是否有 JSON 回應。要理解請求 URL、Method、Query、必要 Headers、Cookies、回應結構與分頁。不能把私密 token 貼進教材、Git 或公開程式碼。

## webdriver

電腦需安裝 Chrome。現代 Selenium 通常可透過 Selenium Manager 處理適合的 driver；第一次執行可能需要網路與較長時間。公司電腦若有代理、防火牆或禁止下載，請由管理者依組織規範預先配置，不要從不明網站下載 driver。

`webdriver.Chrome()` 背後不是 Python 假裝成瀏覽器，而是 Python Selenium 套件透過 WebDriver 協定控制真正的 Chrome。大致角色：

```text
你的 Python 程式 → Selenium API → ChromeDriver/WebDriver → Chrome → 網站
```

## [第一支Selenium](./Scraping&Selenium_src/第一支Selenium.md)

## [ChromeOptions 與 Headless 模式(有頭與無頭模式)](./Scraping&Selenium_src/無頭模式.md)

Selenium 啟動 Chrome 時，可以透過 `ChromeOptions()` 設定瀏覽器的啟動方式。

```python
options = webdriver.ChromeOptions()
options.add_argument("--headless=new") # 使用無頭模式，不顯示 Chrome 視窗
options.add_argument("--window-size=1280,900") # 固定瀏覽器視窗尺寸
driver = webdriver.Chrome(options=options) # Selenium 就會按照這些設定啟動 Chrome。
```

流程會變成：

```
Python
  ↓
Selenium
  ↓
Chrome 在背景執行
  ↓
沒有瀏覽器視窗顯示
```

## 定位與操作元素

### [find_element 與 find_elements](./Scraping&Selenium_src/find_element.md)

| 方法            | 找到              | 找不到                        |
| --------------- | ----------------- | ----------------------------- |
| `find_element`  | 第一個 WebElement | 拋出 `NoSuchElementException` |
| `find_elements` | WebElement 清單   | 空清單                        |

Selenium 的 WebElement 是瀏覽器中「活的元素參照」；BeautifulSoup 的 Tag 是某份 HTML 快照裡的節點。JavaScript 改掉 DOM 後，舊 WebElement 可能失效，產生 `StaleElementReferenceException`。

```python
### 定位方式
driver.find_element(By.ID, "search")
driver.find_element(By.NAME, "keyword")
driver.find_element(By.CSS_SELECTOR, ".job-card .detail-button")
driver.find_element(By.XPATH, "//button[contains(., '載入更多')]")
```

使用方式沿用 BeautifulSoup 的 CSS Selector，因為一套知識可同時用在兩邊。穩定性通常優先考慮語意清楚的 `id`、`name`、`data-*` 或 class；避免依賴第幾個 div、視覺位置、隨機產生的 class。

### 讀取與操作

```python
element.text                       # 畫面可見文字
element.get_attribute("href")      # 屬性值
element.get_property("value")     # DOM property
element.is_displayed()             # 是否顯示
element.is_enabled()               # 是否可操作
element.click()                    # 點擊
element.send_keys("Python")        # 輸入
element.clear()                    # 清除欄位
```

下拉選單使用 `Select` 更能表達目的：

```python
from selenium.webdriver.support.ui import Select
Select(driver.find_element(By.ID, "city")).select_by_visible_text("臺中市")
```

- [範例：讀取元素資料](./Scraping&Selenium_src/讀取元素資料.md)
- [範例：操作輸入框與按鈕](./Scraping&Selenium_src/操作輸入框與按鈕.md)
- [範例：操作下拉選單：操作中華郵政縣市下拉選單為例](./Scraping&Selenium_src/操作下拉選單.md)

## 等待是 Selenium 的核心

### 為什麼 `driver.get()` 完成還不夠

瀏覽器完成初始頁面載入，不代表後續 JavaScript 已取得資料。程式與網站像兩位跑者：有時網站先到，有時程式先到，便形成 race condition。這就是「昨天能跑、今天偶爾壞」的常見根源。

- [(不推薦)第一種：用固定sleep當主要等待](./Scraping&Selenium_src/用固定sleep當主要等待.md)
- [第二種：隱含等待implicitly_wait](./Scraping&Selenium_src/隱含等待implicitly_wait.md)
- [(推薦)第三種：明確等待WebDriverWait](./Scraping&Selenium_src/明確等待WebDriverWait.md)

## 實作

- [基於selenium對104爬蟲](./Scraping&Selenium_src/基於s\elenium對104爬蟲.md)
- [Quotes_to_Scrape延遲載入頁面](./Scraping&Selenium_src/Quotes_to_Scrape延遲載入頁面.md)
