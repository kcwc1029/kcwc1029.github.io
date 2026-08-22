## HW要求

目標網站：https://the-internet.herokuapp.com/dynamic_controls

這個頁面可以動態移除核取方塊，也能啟用或停用輸入框。請用 Selenium 觀察元素狀態改變。

核取方塊部分：

- 確認核取方塊是否顯示。
- 保存核取方塊 WebElement。
- 點擊 Remove。
- 等待舊核取方塊 stale。
- 確認提示訊息出現。
- 點擊 Add，等待新核取方塊出現。

輸入框部分：

- 使用 is_enabled() 確認輸入框目前不可操作。
- 點擊 Enable。
- 等待輸入框可以操作。
- 輸入 Python Selenium。
- 讀取輸入框的 value。
- 點擊 Disable。
- 確認輸入框再次停用。
