```py
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote
# quote() 會幫忙處理中文、空白及特殊符號。像是輸入：人工智慧
# 會轉成瀏覽器能正確辨識的網址格式，再交給 requests 發送請求。


### 讓使用者輸入搜尋主題
keyword = input("請輸入想爬取的維基百科主題：").strip()

if not keyword:
    print("沒有輸入搜尋主題")
    raise SystemExit


### 設定網址
encoded_keyword = quote(keyword) # 將中文及空白轉換成網址可使用的格式
url = f"https://zh.wikipedia.org/wiki/{encoded_keyword}"

headers = {
    "User-Agent": "Mozilla/5.0"
}


### 發送 HTTP 請求
response = requests.get(
    url,
    headers=headers,
    timeout=10
) # 向 Wikipedia 發送 GET 請求，最多等待 10 秒

response.raise_for_status() # 如果請求失敗 (4xx、5xx)，直接拋出例外

print("狀態碼：", response.status_code)
print("爬取網址：", response.url)


### 建立 BeautifulSoup
soup = BeautifulSoup(
    response.text,
    "lxml"
) # 將取得的 HTML 原始碼交給 BeautifulSoup 解析


### 檢查維基百科是否找到頁面
no_article = soup.select_one(".noarticletext")

if no_article:
    print(f"找不到「{keyword}」的維基百科頁面")
    raise SystemExit


### 抓取頁面標題
title = soup.select_one("h1") # 使用 CSS Selector 找到第一個 <h1>

if title:
    title_text = title.get_text(strip=True)

    print("\n頁面標題：")
    print(title_text)

else:
    title_text = keyword


### 建立安全的檔案名稱
file_name = re.sub(
    r'[\\/:*?"<>|]',
    "_",
    title_text
) # 將 Windows 檔名不能使用的符號替換成底線


### 抓取右側基本資料表
info_list = []
info_table = soup.select_one(
    "table.infobox"
) # 找到 Wikipedia 右側的 infobox 資料表

if info_table:
    rows = info_table.select("tr") # 取得資料表中的所有列

    for row in rows:
        field = row.select_one("th") # <th> 通常是欄位名稱
        value = row.select_one("td") # <td> 通常是欄位內容

        if field and value:
            field_text = field.get_text(
                " ",
                strip=True
            ) # 取得欄位名稱

            value_text = value.get_text(
                " ",
                strip=True
            ) # 取得欄位內容

            info_list.append({
                "欄位": field_text,
                "內容": value_text
            })


### 顯示基本資料
print("\n基本資料：")

if info_list:
    for item in info_list:
        print(f"{item['欄位']}：{item['內容']}")

else:
    print("這個頁面沒有右側基本資料表")


### 儲存基本資料 CSV
if info_list:
    info_df = pd.DataFrame(
        info_list
    ) # 將基本資料轉換成 DataFrame

    info_df.to_csv(
        f"{file_name}_基本資料.csv",
        index=False,
        encoding="utf-8-sig"
    ) # 使用 utf-8-sig，避免使用 Excel 開啟中文 CSV 時出現亂碼


### 抓取章節標題
print("\n文章章節：")

headings = soup.select(
    ".mw-parser-output h2, "
    ".mw-parser-output h3"
) # 同時取得文章中的 h2 與 h3 標題

for heading in headings:
    heading_text = heading.get_text(
        " ",
        strip=True
    ) # 取得章節標題文字

    print(heading_text)


### 抓取文章內文
paragraph_list = []
paragraphs = soup.select(
    ".mw-parser-output > p"
) # 取得文章主要內容區域第一層的 <p>

for paragraph in paragraphs:
    text = paragraph.get_text(
        " ",
        strip=True
    ) # 取得段落文字並移除前後空白

    if text: # 排除沒有文字的空白段落
        paragraph_list.append(text)


### 顯示文章內文
print("\n文章內文：")

for paragraph in paragraph_list:
    print(paragraph)
    print()


### 儲存文章內文
with open(
    f"{file_name}_文章內文.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        f"標題：{title_text}\n\n"
    ) # 寫入文章標題

    for paragraph in paragraph_list:
        file.write(
            paragraph + "\n\n"
        ) # 每個段落之間空一行


### 執行完成
print("資料抓取完成")

if info_list:
    print(f"已產生：{file_name}_基本資料.csv")

print(f"已產生：{file_name}_文章內文.txt")
```
