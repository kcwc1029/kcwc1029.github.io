爬取網站：https://quotes.toscrape.com/js-delayed/ (用專門提供爬蟲練習的)

它會透過 JavaScript 延遲產生 10 筆名言，剛好能清楚示範 WebDriverWait。

```py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


### 設定網址
url = "https://quotes.toscrape.com/js-delayed/"


### 設定 Chrome 瀏覽器
options = webdriver.ChromeOptions()

options.add_argument("--window-size=1280,900") # 固定瀏覽器視窗尺寸
options.page_load_strategy = "eager" # HTML 載入完成後就繼續，不等待所有資源


### 啟動 Chrome
driver = webdriver.Chrome(options=options)


### 定義等待條件
def wait_for_10_quotes(driver):
    quote_elements = driver.find_elements(
        By.CSS_SELECTOR,
        ".quote"
    ) # 尋找目前已經建立的名言區塊

    print(
        f"目前找到：{len(quote_elements)} 筆",
        end="\r"
    )

    if len(quote_elements) >= 10:
        return quote_elements # 達到 10 筆時，回傳元素清單

    return False # 未達 10 筆時，讓 WebDriverWait 繼續等待


### 開啟網頁
try:
    print("正在開啟名言網站...")

    driver.get(url)

    print("網頁開啟完成，開始等待動態資料")


    ### 立即尋找資料
    quotes_before_wait = driver.find_elements(
        By.CSS_SELECTOR,
        ".quote"
    )

    print("\n等待前找到的資料數量：")
    print(len(quotes_before_wait))


    ### 等待至少出現 10 筆資料
    wait = WebDriverWait(
        driver,
        15,
        poll_frequency=0.5
    ) # 每 0.5 秒檢查一次，最多等待 15 秒

    quote_elements = wait.until(
        wait_for_10_quotes
    )


    ### 顯示等待後的資料數量
    print("\n")
    print("動態資料載入完成")
    print(f"等待後找到的資料數量：{len(quote_elements)}")


    ### 擷取前 10 筆資料
    print("\n前 10 筆名言：")

    for index, quote in enumerate(quote_elements[:10], start=1):
        quote_text = quote.find_element(
            By.CSS_SELECTOR,
            ".text"
        ).text # 取得名言內容

        author = quote.find_element(
            By.CSS_SELECTOR,
            ".author"
        ).text # 取得作者名稱

        print(f"\n第 {index} 筆")
        print(f"名言：{quote_text}")
        print(f"作者：{author}")


except TimeoutException:
    print("\n等待超過 15 秒")
    print("動態資料沒有成功載入")

    driver.save_screenshot(
        "名言網站_等待失敗.png"
    )

    print("已儲存畫面：名言網站_等待失敗.png")


finally:
    driver.quit()


### 執行完成
print("\n瀏覽器已關閉")
```
