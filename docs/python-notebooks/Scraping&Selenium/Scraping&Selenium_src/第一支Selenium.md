```python
from selenium import webdriver

driver = webdriver.Chrome()
try:
    driver.get("https://www.youtube.com/")
    print(driver.title)
finally:
    driver.quit()
```

- `driver` 是這次瀏覽器工作階段的控制器。
- `get()` 導航到網址。
- `title`、`current_url` 是目前頁面狀態。
- `quit()` 關閉整個工作階段與所有視窗。
- `finally` 保證即使中途錯誤仍會關閉，避免教室留下十幾個背景 Chrome。

`close()` 只關閉目前視窗；`quit()` 結束整個 session。爬蟲通常在工作結束使用 `quit()`。
