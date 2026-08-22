隱含等待會告訴 Selenium：找不到元素時，最多再等幾秒。

設定一次後，後面的 find_element() 與 find_elements() 都會受到影響。

```py
driver.implicitly_wait(10)
```

這不是每次都固定停 10 秒。若元素在第 2 秒出現，Selenium 就會立刻繼續；只有一直找不到時，才會等到接近 10 秒。

```py
from selenium import webdriver
from selenium.webdriver.common.by import By


### 啟動 Chrome
driver = webdriver.Chrome()

driver.implicitly_wait(10) # 找不到元素時，最多等待 10 秒


### 開啟網頁
try:
    driver.get("https://zh.wikipedia.org/wiki/臺灣")


    ### 取得文章標題
    title = driver.find_element(
        By.ID,
        "firstHeading"
    )

    print("文章標題：")
    print(title.text)


    ### 取得文章段落
    paragraph = driver.find_element(
        By.CSS_SELECTOR,
        ".mw-content-ltr > p"
    )

    print("\n第一段內容：")
    print(paragraph.text)


finally:
    driver.quit()
```

它的優點是寫法簡單，但只能處理「元素是否找得到」，不能精確表達更多條件，例如：

- 元素已經顯示
- 按鈕已經可以點擊
- 指定文字已經出現
- Loading 遮罩已經消失
- 舊的搜尋結果已經更新
