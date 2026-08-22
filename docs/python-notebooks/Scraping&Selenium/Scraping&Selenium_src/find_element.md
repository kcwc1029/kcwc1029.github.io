```py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


### 設定 Chrome 瀏覽器
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1280,900") # 固定瀏覽器視窗尺寸


### 啟動 Chrome
driver = webdriver.Chrome(options=options)


### 開啟網頁
try:
    url = "https://zh.wikipedia.org/wiki/臺灣"

    driver.get(url)

    print("網頁標題：")
    print(driver.title)


    ### find_element：取得第一個符合條件的元素
    page_title = driver.find_element(
        By.ID,
        "firstHeading"
    ) # 透過 id 找到頁面主標題

    print("\n文章標題：")
    print(page_title.text)


    ### find_element：取得第一段文章內容
    first_paragraph = driver.find_element(
        By.CSS_SELECTOR,
        ".mw-content-ltr > p"
    ) # 找到文章內容區域裡的第一個段落

    print("\n第一段內容：")
    print(first_paragraph.text)


    ### find_elements：取得所有章節標題
    heading_elements = driver.find_elements(
        By.CSS_SELECTOR,
        ".mw-heading2 h2"
    ) # 找到文章中的所有第二層章節標題

    print("\n章節數量：", len(heading_elements))

    print("\n文章章節：")

    for heading in heading_elements:
        print(heading.text)


    ### find_elements 找不到時會回傳空清單
    missing_elements = driver.find_elements(
        By.CSS_SELECTOR,
        ".not-exist"
    )

    print("\n不存在的元素數量：")
    print(len(missing_elements)) # 輸出 0


    ### find_element 找不到時會拋出例外
    try:
        missing_element = driver.find_element(
            By.ID,
            "not-exist"
        )

    except NoSuchElementException:
        print("find_element 找不到指定元素")


finally:
    driver.quit()


### 執行完成
print("\n瀏覽器已關閉")
```
