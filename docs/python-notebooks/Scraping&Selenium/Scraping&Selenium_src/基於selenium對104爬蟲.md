會跑得比較慢(要等個五分鐘)

```py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


### 設定網址
url = "https://www.104.com.tw/jobs/search/?keyword=Python"


### 設定 Chrome 瀏覽器
options = webdriver.ChromeOptions()

options.add_argument("--window-size=1280,900") # 固定瀏覽器視窗尺寸
options.page_load_strategy = "none" # HTML 載入完成後就繼續，不等待所有圖片


### 啟動 Chrome
driver = webdriver.Chrome(options=options)

driver.set_page_load_timeout(20) # 整個網頁最多載入 20 秒


### 定義等待條件
def wait_for_12_jobs(driver):
    job_elements = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/job/']"
    ) # 找出網址中包含 /job/ 的職缺連結

    visible_jobs = [
        job
        for job in job_elements
        if job.is_displayed() and job.text.strip()
    ] # 排除隱藏或沒有文字的連結

    if len(visible_jobs) >= 12:
        return visible_jobs # 達到 12 筆時，將元素清單傳回去

    return False # 未達 12 筆時，讓 WebDriverWait 繼續等待


### 開啟網頁
try:
    driver.get(url)

    print("網頁標題：")
    print(driver.title)


    ### 立即尋找職缺
    jobs_before_wait = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/job/']"
    )

    print("\n等待前找到的職缺連結數量：")
    print(len(jobs_before_wait))


    ### 等待至少出現 12 筆職缺
    wait = WebDriverWait(driver, 15)

    job_elements = wait.until(
        wait_for_12_jobs
    )

    print("\n等待後找到的有效職缺數量：")
    print(len(job_elements))


    ### 顯示前 12 筆職缺
    print("\n前 12 筆 Python 職缺：")

    for index, job in enumerate(job_elements[:12], start=1):
        job_title = job.text.strip()
        job_url = job.get_attribute("href")

        print(f"\n第 {index} 筆")
        print(f"職缺名稱：{job_title}")
        print(f"職缺網址：{job_url}")


except TimeoutException:
    print("\n等待超過 15 秒")
    print("職缺資料可能尚未載入，或網站結構已經改變")


finally:
    driver.quit()


### 執行完成
print("\n瀏覽器已關閉")
```
