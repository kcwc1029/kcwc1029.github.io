from selenium import webdriver

driver = webdriver.Chrome()
try:
    driver.get("https://example.com")
    print(driver.title)
finally:
    driver.quit()