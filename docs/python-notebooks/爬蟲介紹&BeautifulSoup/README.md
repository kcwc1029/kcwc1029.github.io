# Python 爬蟲介紹與 BeautifulSoup

> 適用對象：職業訓練、第一次接觸網頁技術的學員  
> 開發環境：VS Code、uv、Python 3.11 以上  
> 教材定位：從「看得懂網頁」到「把 72 筆職缺整理成表格」  
> 範例資料皆為教學用虛構資料，不需要連外即可練習。

---

## 教師使用說明

這份教材刻意把技術講得比較慢。每遇到一個新名詞，先用生活類比，再看 HTML，最後才寫 Python。學生若問「這可以幹嘛」，可以先回答：

- 求職時，自動整理公開職缺的地區、技能與薪資，減少逐頁抄寫。
- 租屋時，整理公開物件後比較區域行情，但要遵守網站規定。
- 比價時，把公開商品價格做成自己的觀察表。
- 行政工作中，把重複貼到 Excel 的資料自動化。
- 行銷工作中，整理公開活動、標題或新聞資料，再做分類與統計。

爬蟲不是「破解網站」，而是讓程式代替人完成「下載公開頁面、找到需要的欄位、整理成資料」這三件事。能不能爬與該不該爬是兩個問題；技術做得到，不代表網站規定或法律允許。

### 建議授課節奏

每段可以重複使用「預測 → 執行 → 解釋 → 改錯」：

1. 先不執行，讓學生猜輸出。
2. 執行範例，觀察實際結果。
3. 請學生用自己的話解釋每一行。
4. 故意把選擇器改錯，練習從空結果找原因。
5. 換一個條件，讓學生確認自己不是只會照抄。

---

# 第一部分：爬蟲到底在做什麼

## 1. 從「人工抄資料」開始想

假設你正在找工作。你打開職缺網站，看見 72 張職缺卡片，想回答：

- 哪些工作接受無經驗？
- 哪些工作最低薪資超過 35,000 元？
- 台中有哪些 Python 相關職缺？
- 哪個技能在這批職缺最常出現？

人工做法是打開每一筆、複製、貼到 Excel。這很像請一個人做 72 次相同動作。爬蟲則是把這套規則寫成程式：

```text
取得網頁 → 看懂 HTML 結構 → 找到每張卡片 → 取出欄位 → 清理 → 儲存
```

爬蟲的英文常見為 Web Scraping。Scrape 原意有「刮取」，可以想像成從一大張佈告欄上，把你需要的公開資訊刮下來，整理進自己的表格。

### 課堂提問

1. 如果只有 3 筆資料，值得寫程式嗎？
2. 如果每天都要整理 3 筆，連續一年呢？
3. 如果網站明天改版，人工和程式各自會遇到什麼問題？

關鍵不是資料「現在有幾筆」，而是工作是否重複、規則是否清楚，以及未來會不會再次執行。

## 2. 網頁、網站與伺服器

初學者常把三個概念混在一起：

- 網站：像一間百貨公司。
- 網頁：百貨公司裡的一個櫃位或一張目錄。
- 伺服器：保管資料並接受請求的後場人員。
- 瀏覽器：替使用者送出請求、把回應畫成畫面的工具。

當你輸入網址並按 Enter，大致發生以下事情：

```text
你的瀏覽器                         網站伺服器
     |                                 |
     |---- HTTP Request：請給我頁面 --->|
     |                                 |
     |<--- HTTP Response：狀態＋內容 ----|
     |                                 |
     ↓
把 HTML、CSS、JavaScript 呈現在螢幕上
```

爬蟲程式通常扮演一個簡化版瀏覽器。`requests` 負責「去拿」，BeautifulSoup 負責「在拿回來的 HTML 裡尋找」。

> 記憶口訣：Requests 是外送員，BeautifulSoup 是整理員。  
> 外送員把箱子拿回來，整理員才知道箱子裡哪些是商品、價格與地址。

## 3. HTTP 請求與回應

HTTP 是瀏覽器與伺服器溝通的規則。像去餐廳點餐：

- URL：桌號加上餐點名稱，表示要找哪個資源。
- Method：動作；`GET` 通常是讀取，`POST` 常用於提交。
- Headers：附註，例如接受的格式、瀏覽器資訊。
- Body：要送出的主要內容，GET 通常沒有。
- Status Code：店家回覆的處理結果。

常見狀態碼：

| 狀態碼  | 白話意思           | 程式應對                 |
| ------- | ------------------ | ------------------------ |
| 200     | 成功拿到內容       | 繼續解析                 |
| 301/302 | 資源搬家，請到別處 | requests 通常會跟隨轉址  |
| 403     | 伺服器拒絕         | 停下來檢查規範，不要硬闖 |
| 404     | 找不到頁面         | 檢查網址或記錄缺漏       |
| 429     | 請求太頻繁         | 降低頻率、尊重限制       |
| 500     | 伺服器內部出錯     | 稍後再試，設定重試上限   |

`response.status_code == 200` 不代表資料一定正確。伺服器也可能回傳登入頁、驗證頁或「查無資料」的 HTML。所以除了狀態碼，也要檢查頁面標題、資料筆數與必要欄位。

## 4. 靜態與動態網頁

這是爬蟲課最重要的判斷之一。

### 靜態內容

伺服器回來的 HTML 裡已經有商品名稱、價格。BeautifulSoup 讀得到。

### 動態內容

伺服器先回傳空殼，瀏覽器執行 JavaScript 後再取得資料。你在畫面看得到，`requests.get()` 的文字裡卻找不到。

生活類比：

- 靜態網頁像便當：打開盒子，飯菜都在。
- 動態網頁像火鍋材料單：先拿到鍋子，稍後才由別人把食材送上來。

BeautifulSoup 只負責解析收到的 HTML，不會執行 JavaScript。遇到動態網站時，應先用瀏覽器開發者工具的 Network 面板了解資料來源。若網站提供正式 API，通常優先依其規範使用 API。瀏覽器自動化是另一門課，不要一看到空資料就立刻換工具。

---

# 第二部分：合法、合宜、可靠

## 5. 寫程式之前的五個檢查

1. 資料是否公開？是否需要登入、付費或繞過驗證？
2. 網站服務條款是否允許自動化存取？
3. `robots.txt` 提供了什麼爬取指引？
4. 是否包含姓名、電話、地址、帳號等個人資料？
5. 請求頻率是否會造成對方負擔？

`robots.txt` 是網站給自動化程式的爬取指引，但它不是法律同意書，也不是看到允許就代表任何用途都合法。仍要看服務條款、資料授權、個資與著作權。

### 教學專案的安全原則

- 優先使用本教材提供的本機 HTML。
- 真實網站只做少量、公開、允許的示範。
- 設定 `timeout`，避免永久等待。
- 說明 `User-Agent`，不要假冒不相關身分。
- 控制頻率，能快取就不重複下載。
- 不繞過登入、驗證碼、付費牆或存取控制。
- 不收集完成任務所不需要的個資。

### 可以討論的職場情境

主管說：「競爭對手網站都公開，你全部抓回來就好。」工程師仍要確認用途、規定與資料範圍。專業不只是會寫，而是知道何時應停下來詢問。

---

# 第三部分：建立 uv＋VS Code 專案

## 6. uv 是什麼

Python 專案通常需要：

- 指定 Python 版本；
- 建立彼此隔離的虛擬環境；
- 安裝套件；
- 記錄版本，讓別台電腦重現。

uv 把這些常用工作整合起來。虛擬環境可想成每個專案自己的工具箱：A 專案要新版套件、B 專案要舊版套件，彼此不打架。

本教材已提供 `pyproject.toml`。在 VS Code 開啟本資料夾後，於終端機執行：

```powershell
uv sync
```

它會同步依賴並建立 `.venv`。接著在 VS Code：

1. 按 `Ctrl+Shift+P`。
2. 輸入 `Python: Select Interpreter`。
3. 選擇本專案 `.venv` 裡的 Python。

執行程式：

```powershell
uv run python examples/01_第一支BeautifulSoup.py
```

若要從零建立另一個專案：

```powershell
uv init 我的爬蟲專案
cd 我的爬蟲專案
uv add requests beautifulsoup4
```

### 常見混淆

- 安裝套件名稱是 `beautifulsoup4`。
- Python 匯入名稱是 `bs4`。
- 類別名稱是 `BeautifulSoup`。

三者長得不同，但指向同一套工具。這不是打錯字。

---

# 第四部分：先讀懂 HTML

## 7. HTML 是有結構的文字

以下是一張商品卡：

```html
<article class="product" data-id="P001">
  <h2 class="name">炙燒雞腿便當</h2>
  <span class="price">120</span>
  <a href="/product/P001">查看餐點</a>
</article>
```

拆解第一行：

```text
<article class="product" data-id="P001">
    ↑          ↑                 ↑
  標籤名      class 屬性          自訂屬性
```

- 標籤 Tag：說明內容角色，例如 `h1` 是主標題、`a` 是連結。
- 屬性 Attribute：附加資訊，例如 `href`、`class`、`id`。
- 文字 Text：人真正看到的「炙燒雞腿便當」。
- 巢狀 Nesting：一個標籤可以包住其他標籤。

## 8. DOM 樹

BeautifulSoup 不是把 HTML 當普通長字串，而是解析成樹：

```text
article.product
├── h2.name
│   └── "炙燒雞腿便當"
├── span.price
│   └── "120"
└── a
    └── "查看餐點"
```

家族關係的說法很適合 DOM：

- `article` 是三個標籤的 parent（父元素）。
- `h2`、`span`、`a` 是 children（子元素）。
- 三者彼此是 siblings（兄弟元素）。
- 更外層還有 ancestors（祖先元素）。

為什麼要懂樹？因為「找頁面上所有 span」太寬了；更可靠的說法是「每張 job-card 裡，找 salary」。先鎖定一張卡，再在卡內找欄位，資料才不會配錯。

## 9. id 與 class

可以把 `id` 想成身分證號，同一頁理論上應唯一；把 `class` 想成社團名稱，許多元素可以加入同一社團。

```html
<h1 id="site-title">轉職雷達</h1>
<article class="job-card remote">...</article>
```

`article` 同時有 `job-card` 與 `remote` 兩個 class。BeautifulSoup 的 `tag.get("class")` 通常會得到清單，而不是單一字串。

---

# 第五部分：BeautifulSoup 核心操作

## 10. 解析第一份 HTML

檔案：`examples/01_第一支BeautifulSoup.py`

```python
from pathlib import Path
from bs4 import BeautifulSoup

html = Path("datasets/迷你商店.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")
```

逐行理解：

1. `Path` 幫我們處理檔案路徑。
2. `read_text()` 把檔案讀成 Python 字串。
3. `encoding="utf-8"` 告訴 Python 如何把位元組翻譯成繁體中文。
4. `BeautifulSoup(html, "html.parser")` 把字串解析成樹。

`html.parser` 是 Python 內建解析器，課堂環境最省事。真實世界還有 `lxml` 等解析器，速度與容錯可能不同；團隊應固定解析器並測試，避免不同電腦出現不同結果。

## 11. find() 與 find_all()

```python
title = soup.find("h1")
cards = soup.find_all("article", class_="product")
```

| 方法         | 回傳              | 找不到時    | 適用               |
| ------------ | ----------------- | ----------- | ------------------ |
| `find()`     | 第一個 Tag        | `None`      | 頁面標題、單一欄位 |
| `find_all()` | ResultSet，像清單 | 空清單 `[]` | 多張卡片、多個連結 |

為什麼是 `class_` 而不是 `class`？因為 `class` 已經是 Python 的保留字，所以 BeautifulSoup 使用尾端底線避開衝突。

### 最常見錯誤

```python
title = soup.find("h9")
print(title.text)
```

如果根本沒有 `h9`，`title` 是 `None`，再取 `.text` 就會出現：

```text
AttributeError: 'NoneType' object has no attribute ...
```

安全寫法：

```python
title = soup.find("h9")
if title is None:
    print("找不到標題，請檢查 HTML 或選擇條件")
else:
    print(title.get_text(strip=True))
```

錯誤訊息不是責罵，而是線索：程式以為手上有標籤，實際拿到的是「沒有東西」。

## 12. 取得文字與屬性

```python
name = tag.get_text(" ", strip=True)
href = link.get("href", "")
job_id = card["data-job-id"]
```

- `.get_text()` 收集標籤裡的人類可見文字。
- `strip=True` 移除頭尾多餘空白。
- 第一個參數 `" "` 表示多段文字間用空格連接。
- `tag["href"]` 不存在時會出錯。
- `tag.get("href", "")` 不存在時回傳空字串，適合真實髒資料。

何時該讓程式出錯？若 `data-job-id` 是資料絕對不可缺的主鍵，缺少時立刻出錯反而能早點發現品質問題。若是可選的圖片網址，使用預設值較合理。

## 13. CSS 選擇器

CSS 選擇器本來是前端工程師用來指定「哪些元素要套樣式」，爬蟲也可用同一套語法找資料。

```python
soup.select("article.job-card")       # 所有符合者
soup.select_one("#site-title")        # 第一個符合者
soup.select(".job-card .salary")      # 卡片內的薪資
soup.select("article.remote")         # 同時是 article 且有 remote class
soup.select("[data-job-id='J009']")   # 指定屬性值
```

常用符號：

| 選擇器         | 意思               | 例子                      |
| -------------- | ------------------ | ------------------------- |
| `tag`          | 標籤名             | `article`                 |
| `.class`       | class              | `.job-card`               |
| `#id`          | id                 | `#site-title`             |
| `A B`          | A 裡面的任意後代 B | `.job-card .salary`       |
| `A > B`        | A 的直接子元素 B   | `article > h2`            |
| `[attr]`       | 有某屬性           | `[datetime]`              |
| `[attr=value]` | 屬性值相同         | `[data-job-id='J001']`    |
| `:not(...)`    | 排除條件           | `.product:not(.sold-out)` |

### 選擇器閱讀練習

請從右往左讀：

```css
section#job-list article.job-card h2.job-title
```

「找 class 是 job-title 的 h2；它在 class 是 job-card 的 article 裡；而 article 又在 id 是 job-list 的 section 裡。」

### find 還是 select？

沒有唯一正解。簡單找單一標籤時 `find()` 很直觀；已會 CSS 或條件涉及階層時，`select()` 常更好讀。團隊重點是保持一致與可維護，不是比誰寫得最短。

---

# 第六部分：從網頁變成可分析資料

## 14. 先建立 72 筆本機職缺網站

```powershell
uv run python examples/00_建立本機練習網站.py
```

資料來源是 `datasets/職缺資料_72筆.csv`，執行後會建立 `datasets/職缺市集.html`。

為什麼教材不直接爬真實求職網站？

- 真實網站可能有禁止自動化的條款。
- 版面可能在上課前一晚改掉。
- 教室網路可能不穩。
- 有些網站由 JavaScript 動態載入。
- 本機資料可重複實驗，所有學生得到相同答案。

這不是「假爬蟲」。HTML 解析、選擇器、清理、驗證與輸出流程都與真實工作相同，只是把不穩定的下載步驟隔離。

## 15. 一張卡片一筆資料

檔案：`examples/04_解析72筆職缺.py`

核心模式：

```python
jobs = []

for card in soup.select("article.job-card"):
    job = {
        "職缺": card.select_one(".job-title").get_text(strip=True),
        "公司": card.select_one(".company").get_text(strip=True),
    }
    jobs.append(job)
```

請注意搜尋範圍是 `card.select_one(...)`，不是每次都從 `soup` 搜。這像先拿起一張履歷，再從同一張履歷讀姓名和電話；如果分別從整疊履歷找第一個姓名、第一個電話，有機會把不同人的資料配在一起。

## 16. 資料型別清理

網頁文字通常是字串：

```python
salary_text = "月薪 40,000 元"
```

要排序與計算，就要變成整數。教材頁面特別把純數字放在 `data-min`：

```python
min_salary = int(salary_tag.get("data-min", 0))
```

真實網站沒有乾淨屬性時，可做清理：

```python
text = "月薪 40,000 元"
number = int(text.replace("月薪", "").replace("元", "").replace(",", "").strip())
```

但要小心「面議」「時薪」「年薪」不能全部硬轉。資料清理前要先列出可能格式，再決定規則；不要用一個正規表示式假裝所有情況都一樣。

## 17. 多值欄位

一份職缺可能有多個技能：

```python
skills = [tag.get_text(strip=True) for tag in card.select(".skill")]
```

結果：

```python
["Python", "BeautifulSoup"]
```

清單生成式的完整寫法：

```python
skills = []
for tag in card.select(".skill"):
    skills.append(tag.get_text(strip=True))
```

初學時先寫完整版，看懂「逐一取出 → 清理文字 → 放入清單」，再縮成一行。

## 18. 篩選轉職條件

檔案：`examples/05_篩選適合我的職缺.py`

程式不是替你決定人生，而是先把 72 筆縮成值得人工閱讀的 8 筆。這是資料工具的價值：降低資訊量，把時間留給需要判斷的事。

```python
if "Python" in skills and "不拘" in experience and min_salary >= 35000:
    matched.append(...)
```

可以請學生逐項改條件：

- 把最低薪資改為自己的期待。
- 只看自己的縣市。
- 接受「是」或「部分」遠端。
- 排除自己不想要的技能。

這時學生會立刻感受到「變數與條件判斷」不是考試語法，而是把個人偏好變成可執行規則。

## 19. 輸出 CSV

檔案：`examples/06_輸出CSV.py`

```python
with output_path.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["編號", "職缺", "公司"])
    writer.writeheader()
    writer.writerow({"編號": "J001", "職缺": "Python資料助理", "公司": "好日子數位"})
```

重點：

- `with` 結束時會妥善關閉檔案。
- `newline=""` 避免 Windows CSV 出現多餘空白列。
- `utf-8-sig` 讓常見 Windows Excel 較容易正確辨識繁體中文。
- `writeheader()` 寫欄位名稱。
- 字典 key 要與 `fieldnames` 對得上。

執行：

```powershell
uv run python examples/06_輸出CSV.py
```

完成後用 VS Code 或試算表開啟 `outputs/爬取結果.csv`。

---

# 第七部分：真正下載網頁

## 20. requests 基本流程

檔案：`examples/07_requests取得網頁.py`

```python
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
html = response.text
soup = BeautifulSoup(html, "html.parser")
```

### 為什麼一定寫 timeout

沒有 timeout 時，網路或伺服器異常可能讓程式等非常久。`timeout=10` 表示網路操作超過合理等待就回報錯誤，讓程式有機會記錄、重試或結束。

### 為什麼使用 raise_for_status

如果伺服器回 404，`requests.get()` 本身仍成功完成「請求」，但我們沒有拿到想要的頁面。`raise_for_status()` 會把 4xx、5xx 轉成例外，集中交給錯誤處理。

### 例外處理

```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as error:
    print("網路操作失敗：", error)
```

`try` 不是把錯誤藏起來。好的例外處理要回答：

- 哪個網址失敗？
- 是逾時、拒絕，還是找不到？
- 是否重試？最多幾次？
- 失敗資料是否記錄下來？

無限重試是危險的。若網站一直拒絕，程式就一直增加負擔。

## 21. 網址組合

頁面裡可能只有相對網址：

```html
<a href="/jobs/J001">查看職缺</a>
```

它像「從本站大門往右走」，缺少網域。不要用字串直接相加，應使用：

```python
from urllib.parse import urljoin

full_url = urljoin("https://example.com/jobs/", "/jobs/J001")
```

`urljoin` 能正確處理斜線、相對路徑與完整網址。

## 22. 編碼與亂碼

文字在電腦底層是數字。編碼就是「數字如何對應文字」的字典。寫入時用 A 字典，讀取時卻用 B 字典，就可能看到亂碼。

本機檔案：

```python
Path("資料.html").read_text(encoding="utf-8")
```

網路回應可觀察：

```python
print(response.encoding)
print(response.apparent_encoding)
```

不要看到亂碼就隨便試到能看。應檢查 HTTP header、HTML `<meta charset>` 與來源實際編碼，並用固定測試資料驗證。

---

# 第八部分：讓爬蟲不那麼脆弱

## 23. 網站改一個 class，程式為何就壞

爬蟲依賴網頁結構。若：

```html
<span class="salary">40,000</span>
```

改成：

```html
<span class="pay">40,000</span>
```

原本的 `.salary` 就找不到。這不是 BeautifulSoup 壞掉，而是我們的假設過期。

可靠爬蟲要把假設寫得清楚：

- 預期至少有一張卡片。
- 每張卡片一定有編號。
- 薪資可以缺，但缺少時記為 `None`。
- 頁面標題應包含指定文字。

## 24. 安全取值函式

檔案：`examples/08_穩健爬蟲函式.py`

```python
def safe_text(parent, selector, default=""):
    tag = parent.select_one(selector)
    return tag.get_text(" ", strip=True) if tag else default
```

使用：

```python
title = safe_text(card, ".job-title", "未命名職缺")
salary = safe_text(card, ".salary", "薪資未提供")
```

但不要所有欄位都默默給空字串。否則網站整頁改版時，程式可能輸出 72 筆空資料還說成功。必要欄位應驗證並中止，可選欄位才使用預設值。

## 25. 資料驗證

```python
cards = soup.select(".job-card")
if not cards:
    raise ValueError("找不到任何職缺卡片，頁面可能改版")

if len(cards) < 60:
    print("警告：資料量比預期少，請人工檢查")
```

還可以檢查：

- 編號是否重複；
- 薪資是否為合理正數；
- 日期能否解析；
- 缺漏率是否突然升高；
- 本次筆數是否與前次差異過大。

「程式沒有紅字」只代表程式跑完，不代表資料正確。

## 26. 除錯六步驟

當結果是空清單，不要立刻亂改：

1. 確認拿到的真的是目標頁，不是登入或錯誤頁。
2. 印出 `response.status_code` 與前 500 個字。
3. 把 HTML 存檔，用 VS Code 搜尋你在畫面看到的文字。
4. 確認資料是否由 JavaScript 後載入。
5. 在開發者工具測試 CSS 選擇器。
6. 從寬到窄：先找 `article`，再找 `.job-card`，最後加父子關係。

推薦暫時加入：

```python
print("HTML 長度：", len(html))
print("卡片數：", len(soup.select(".job-card")))
print(soup.prettify()[:1000])
```

除錯完成後，移除大量輸出或改用正式 logging。

---

# 第九部分：課堂示範與練習

## 27. 範例檔案地圖

| 檔案                        | 學習焦點                 | 有感情境           |
| --------------------------- | ------------------------ | ------------------ |
| `00_建立本機練習網站.py`    | CSV 轉 HTML、產生測試頁  | 建立自己的職缺網站 |
| `01_第一支BeautifulSoup.py` | 解析、find、find_all     | 找晚餐便當         |
| `02_find與屬性.py`          | id、class、data、href    | 商品編號與連結     |
| `03_CSS選擇器.py`           | select、select_one、排除 | 排除售完便當       |
| `04_解析72筆職缺.py`        | 卡片迴圈、結構化字典     | 轉職資料整理       |
| `05_篩選適合我的職缺.py`    | 條件篩選                 | 薪資與無經驗條件   |
| `06_輸出CSV.py`             | Excel 可開啟的輸出       | 工作報表           |
| `07_requests取得網頁.py`    | HTTP、timeout、例外      | 真正取得公開頁面   |
| `08_穩健爬蟲函式.py`        | 缺漏處理                 | 遇到未提供薪資     |

依序執行：

```powershell
uv run python examples/00_建立本機練習網站.py
uv run python examples/01_第一支BeautifulSoup.py
uv run python examples/02_find與屬性.py
uv run python examples/03_CSS選擇器.py
uv run python examples/04_解析72筆職缺.py
uv run python examples/05_篩選適合我的職缺.py
uv run python examples/06_輸出CSV.py
uv run python examples/07_requests取得網頁.py
uv run python examples/08_穩健爬蟲函式.py
```

## 28. 練習一：今天便當吃什麼

學生檔：`exercises/01_便當選擇器練習.py`  
答案：`answers/01_便當選擇器練習_答案.py`

任務：

1. 印出所有便當名稱與價格。
2. 排除含有 `sold-out` class 的商品。
3. 找出最低價格商品。
4. 顯示商品連結。

### 教師引導，不直接公布答案

- 先用 `.product` 取得每張卡。
- 名稱和價格都在卡片裡找。
- 價格是文字，數字比較前要 `int()`。
- `min()` 可以搭配 `key=` 告訴 Python 比較哪個欄位。

### 延伸

- 設定今天預算，只顯示買得起的便當。
- 若售完商品最便宜，是否應納入推薦？
- 多個商品同價時，`min()` 會怎麼做？

## 29. 練習二：我的轉職雷達

學生檔：`exercises/02_我的轉職雷達.py`  
答案：`answers/02_我的轉職雷達_答案.py`

任務：

1. 選擇縣市。
2. 設定能接受的最低薪資。
3. 依薪資由高到低排序。
4. 顯示職缺、公司與最低薪資。

延伸：

- 使用 `input()` 讓使用者輸入縣市。
- 加入技能關鍵字。
- 顯示完全遠端或部分遠端。
- 將結果輸出 CSV。
- 沒有結果時給友善提示，而不是只印空白。

## 30. 綜合專題：轉職決策助手

### 專題需求

使用 72 筆資料完成：

1. 顯示資料總筆數。
2. 讓使用者輸入縣市、最低薪資、技能。
3. 篩選符合職缺。
4. 依最低薪資由高至低排序。
5. 顯示前 10 筆。
6. 輸出 `outputs/我的職缺清單.csv`。
7. 印出各技能出現次數前 5 名。
8. 缺少欄位時不能整批崩潰。
9. 若完全沒有結果，建議使用者放寬一項條件。

### 評分規準

| 面向       | 比例 | 判斷重點                           |
| ---------- | ---: | ---------------------------------- |
| 正確解析   |  25% | 欄位沒有配錯、72 筆能讀取          |
| 條件與排序 |  20% | 數字型別正確、條件符合需求         |
| 穩健性     |  20% | 找不到元素、空結果、錯誤輸入有處理 |
| 可讀性     |  15% | 命名清楚、函式合理、註解解釋原因   |
| 輸出品質   |  10% | CSV 編碼與欄位正確                 |
| 倫理說明   |  10% | 能說明資料來源、限制與使用界線     |

### 口頭報告問題

- 你的選擇器依賴哪些 HTML 結構？
- 網站把 class 改名後，程式會如何發現？
- 哪些欄位可以缺，哪些不能缺？
- 為什麼儲存最低薪資為整數？
- 真實上線前還需要取得哪些許可或確認？

---

# 第十部分：常見錯誤診療室

## 31. ModuleNotFoundError: No module named 'bs4'

可能原因：VS Code 選到系統 Python，不是專案 `.venv`。

處理：

```powershell
uv sync
uv run python -c "import bs4; print(bs4.__version__)"
```

並重新選擇 VS Code Python Interpreter。

## 32. FileNotFoundError

相對路徑是相對於「執行時所在資料夾」，不一定是程式檔所在資料夾。本教材使用：

```python
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "datasets" / "迷你商店.html"
```

如此從專案根目錄執行時較穩定。

## 33. select() 回傳空清單

檢查：

- class 前是否忘記 `.`？
- id 前是否忘記 `#`？
- 大小寫是否相同？
- HTML 裡真的有資料嗎？
- 取得的是目標頁還是錯誤頁？
- 資料是否由 JavaScript 動態載入？

```python
soup.select("job-card")   # 尋找名為 job-card 的標籤，通常錯
soup.select(".job-card")  # 尋找 class=job-card，正確
```

## 34. TypeError 或 ValueError：不能轉 int

```python
int("40,000")      # 錯，逗號不能直接轉
int("薪資面議")    # 錯，沒有數字
```

先觀察實際格式，再清理與分流。不要只用 `except: pass` 吞掉所有錯誤，否則會不知道遺失了多少資料。

## 35. 中文亂碼

- HTML 本機檔通常用 `encoding="utf-8"`。
- 給 Windows Excel 的 CSV 可用 `utf-8-sig`。
- 不要把「檔案編碼」與「Python 字串」混為一談。
- 檢查來源聲明，不要靠猜。

## 36. AttributeError: NoneType

這幾乎總是在說「前一步沒有找到標籤」：

```python
tag = card.select_one(".salary")
print(tag.get_text())  # tag 可能是 None
```

先印：

```python
print(tag)
print(card.prettify())
```

確認資料真的缺少，還是選擇器寫錯，再決定預設值或中止。

---

# 第十一部分：理解檢核

## 37. 選擇題

1. BeautifulSoup 主要負責什麼？  
   A. 執行 JavaScript　B. 解析 HTML　C. 建立資料庫　D. 自動取得所有權限

2. `find_all()` 找不到資料時通常回傳什麼？  
   A. `None`　B. `0`　C. 空的結果集合　D. 一定拋出錯誤

3. CSS 選擇器 `.job-card .salary` 的意思是什麼？  
   A. 同一元素同時有兩個 class  
   B. job-card 裡的 salary  
   C. salary 的父元素  
   D. id 是 salary

4. 為何請求要設定 timeout？  
   A. 讓網站跑更快　B. 避免無限等待　C. 隱藏身分　D. 自動破解限制

5. HTTP 403 時最合適的第一反應？  
   A. 高速重試　B. 繞過限制　C. 停下檢查規範與權限　D. 忽略狀態碼

答案：1-B、2-C、3-B、4-B、5-C。

## 38. 問答題參考答案

### Requests 與 BeautifulSoup 有何不同？

Requests 負責透過 HTTP 取得內容；BeautifulSoup 把 HTML 解析成可搜尋的樹。前者像取貨，後者像整理貨物。

### 為何畫面看得到，response.text 卻找不到？

內容可能由 JavaScript 在初始 HTML 載入後才取得。應先檢查 Network 與資料來源，不應直接假設 BeautifulSoup 故障。

### 為何爬蟲結果要驗證？

程式能完成不表示抓到正確頁面。登入頁、錯誤頁或改版頁仍可能是合法 HTML，所以要驗證標題、筆數、必要欄位與合理範圍。

### 為何不建議直接從整頁分別抓名稱與價格？

若某張卡缺少價格，兩份清單長度會不同，使用索引配對可能把 A 商品名稱接到 B 商品價格。應先逐張卡片，再在卡片內取欄位。

---

# 第十二部分：教師可用的加深講解

## 39. 為什麼爬蟲最難的常常不是 Python

Python 迴圈可能只有十行，真正花時間的是：

- 理解網站資料如何送到瀏覽器；
- 分辨穩定欄位與純視覺 class；
- 處理缺漏與多種格式；
- 確認授權和合理頻率；
- 發現「看似成功但其實資料錯」；
- 網站改版後維護。

因此職場價值不是背出 `find_all()`，而是能把模糊需求變成資料規格與檢查規則。

## 40. 選擇器要短還是長

太短：

```css
.name
```

頁首使用者名稱、公司名稱、商品名稱都可能被抓到。

太長：

```css
body > main > div:nth-child(2) > section > article:nth-child(1) > h2
```

插入一個廣告區塊就可能失效。

較平衡：

```css
article.job-card .job-title
```

它表達資料的語意與範圍，又不依賴第幾個位置。沒有永遠不壞的選擇器，只能讓假設合理、可測試。

## 41. 爬蟲與 API

API 像餐廳正式菜單與點餐窗口：欄位通常較結構化，規格較清楚。爬 HTML 像從客人看到的擺盤反推食材：能做，但版面原本是給人看，不保證程式介面穩定。

若官方提供符合用途且允許使用的 API，通常優先選 API。若沒有 API，也不能自動推論 HTML 一定可以任意擷取。

## 42. 可重現的重要性

今天抓到的頁面明天可能不同。正式專案可在合規前提下保存：

- 抓取時間；
- 來源網址；
- HTTP 狀態；
- 原始回應或雜湊；
- 解析器版本；
- 程式版本；
- 解析後資料與錯誤清單。

如此資料出問題時，才知道是來源變了、程式變了，還是清理規則變了。

---

# 附錄 A：課堂指令速查

```powershell
# 安裝／同步專案依賴
uv sync

# 建立 72 筆本機網站
uv run python examples/00_建立本機練習網站.py

# 執行單一範例
uv run python examples/04_解析72筆職缺.py

# 執行練習答案
uv run python answers/02_我的轉職雷達_答案.py

# 執行自動測試
uv run pytest -v
```

# 附錄 B：BeautifulSoup 速查表

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

soup.find("h1")                        # 第一個 h1
soup.find_all("a")                     # 所有 a
soup.find(id="site-title")             # 指定 id
soup.find_all("article", class_="job-card")
soup.select_one(".job-card .salary")    # CSS，第一個
soup.select(".job-card .skill")         # CSS，所有

tag.get_text(" ", strip=True)           # 清理文字
tag.get("href", "")                     # 安全讀屬性
tag.name                                # 標籤名
tag.parent                              # 父元素
tag.find_next_sibling()                 # 下一個兄弟元素
```

# 附錄 C：學完後應能做到

- 用自己的話解釋 HTTP 請求與回應。
- 分辨 Requests 與 BeautifulSoup 的責任。
- 看懂基本 HTML 標籤、屬性、id、class 與樹狀關係。
- 使用 `find()`、`find_all()`、`select()`、`select_one()`。
- 安全取得文字與屬性。
- 將多張卡片整理為字典清單。
- 清理數字、多值欄位與缺漏值。
- 輸出繁體中文 CSV。
- 根據狀態碼、HTML 與選擇器逐步除錯。
- 說明靜態與動態網頁的差別。
- 在開始前檢查服務條款、robots 指引、個資與請求頻率。
- 使用 uv 與 VS Code 重現並執行專案。

---

## 官方延伸閱讀

- Beautiful Soup 官方文件：<https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
- uv 專案指南：<https://docs.astral.sh/uv/guides/projects/>
- Python `urllib.robotparser`：<https://docs.python.org/3/library/urllib.robotparser.html>
- Requests 文件：<https://requests.readthedocs.io/>

文件會更新，實務使用時請以官方最新說明為準。
