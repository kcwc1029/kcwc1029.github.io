from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException
)


### 設定搜尋條件
city = "台中市"
keyword = "Python"


### 設定網址
url = (
    "https://job.taiwanjobs.gov.tw/"
    "internet/index/job_search_list.aspx"
)


### 設定 Chrome 瀏覽器
options = webdriver.ChromeOptions()

options.add_argument("--window-size=1920,1080") # 網站建議使用較大的瀏覽器解析度
options.page_load_strategy = "eager" # HTML 載入完成後就繼續


### 啟動 Chrome
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(
    driver,
    20,
    poll_frequency=0.5
)


### 尋找目前顯示的元素
def find_visible_element(by, selector):
    elements = driver.find_elements(by, selector)

    for element in elements:
        if element.is_displayed():
            return element

    raise NoSuchElementException(
        f"找不到顯示中的元素：{selector}"
    )


### 尋找職缺連結
def find_job_links(driver):
    link_elements = driver.find_elements(
        By.XPATH,
        (
            "//a[@href and "
            "contains(translate(@href, "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz'), 'job')]"
        )
    )

    valid_links = []

    for link in link_elements:
        link_text = link.text.strip()
        link_url = link.get_attribute("href")

        if (
            link.is_displayed()
            and link_text
            and link_url
            and len(link_text) >= 2
        ):
            valid_links.append(link)

    return valid_links


### 等待職缺出現
def wait_for_jobs(driver):
    job_links = find_job_links(driver)

    if job_links:
        return job_links

    return False


### 開啟網頁
try:
    print("正在開啟台灣就業通...")

    driver.get(url)

    print("網頁標題：")
    print(driver.title)


    ### 等待首批職缺
    print("\n等待首批職缺...")

    old_job_links = wait.until(
        wait_for_jobs
    )

    print(f"搜尋前找到：{len(old_job_links)} 個職缺連結")


    ### 保存第一個舊元素
    old_job = old_job_links[0]

    print("保存的舊職缺：")
    print(old_job.text.strip())


    ### 找到關鍵字輸入框
    keyword_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                (
                    "//input[contains("
                    "@placeholder, '工作職稱'"
                    ")]"
                )
            )
        )
    )

    keyword_input.clear()
    keyword_input.send_keys(keyword)

    print(f"\n已輸入關鍵字：{keyword}")


    ### 找到台中市選項
    city_element = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                (
                    "//*[self::label or self::button "
                    "or self::span or self::a]"
                    f"[normalize-space()='{city}']"
                )
            )
        )
    )


    ### 將縣市選項捲動到畫面中
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        city_element
    )


    ### 選擇台中市
    try:
        city_element.click()

    except Exception:
        driver.execute_script(
            "arguments[0].click();",
            city_element
        )

    print(f"已選擇工作地點：{city}")


    ### 點擊確認或關閉
    confirm_buttons = driver.find_elements(
        By.XPATH,
        (
            "//button[contains(normalize-space(), '確認/關閉')]"
            " | "
            "//input[contains(@value, '確認/關閉')]"
        )
    )

    for confirm_button in confirm_buttons:
        if confirm_button.is_displayed():
            driver.execute_script(
                "arguments[0].click();",
                confirm_button
            )

            print("已確認工作地點")
            break


    ### 找到主要查詢按鈕
    search_button = find_visible_element(
        By.XPATH,
        (
            "(//button[normalize-space()='查詢']"
            " | "
            "//input[@value='查詢'])[1]"
        )
    )


    ### 點擊查詢
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        search_button
    )

    search_button.click()

    print("已送出查詢，等待搜尋結果更新...")


    ### 等待舊職缺離開 DOM
    wait.until(
        EC.staleness_of(old_job)
    )

    print("舊職缺已離開 DOM")


    ### 重新取得搜尋結果
    new_job_links = wait.until(
        wait_for_jobs
    )

    print(f"\n搜尋條件：{city}、{keyword}")
    print(f"搜尋後找到：{len(new_job_links)} 個職缺連結")


    ### 顯示前 10 筆結果
    print("\n搜尋結果：")

    displayed_urls = set()
    result_count = 0

    for job in new_job_links:
        job_title = job.text.strip()
        job_url = job.get_attribute("href")

        if job_url in displayed_urls:
            continue

        displayed_urls.add(job_url)
        result_count += 1

        print(f"\n第 {result_count} 筆")
        print(f"職缺名稱：{job_title}")
        print(f"職缺網址：{job_url}")

        if result_count >= 10:
            break


    ### 判斷是否沒有資料
    if result_count == 0:
        print("\n搜尋結果為 0 筆")
        print("這可能是搜尋條件的結果，不一定是程式錯誤")


except TimeoutException:
    print("\n等待超過 20 秒")

    driver.save_screenshot(
        "台灣就業通_操作失敗.png"
    )

    print("已儲存畫面：台灣就業通_操作失敗.png")


except NoSuchElementException as error:
    print("\n找不到指定元素：")
    print(error)

    driver.save_screenshot(
        "台灣就業通_找不到元素.png"
    )

    print("已儲存畫面：台灣就業通_找不到元素.png")


finally:
    driver.quit()


### 執行完成
print("\n瀏覽器已關閉")