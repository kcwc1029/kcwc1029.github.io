## HW要求

目標網站：https://webscraper.io/test-sites

你要建立一份電子產品價格比較資料，從分類頁進入商品列表，操作分頁或 Load more，再擷取所有商品資料。

作業要求

Selenium 負責：

- 選擇商品分類
- 點擊子分類
- 操作分頁或 Load more
- 等待新商品出現
- 判斷載入是否結束

BeautifulSoup 負責：

- 商品名稱
- 商品說明
- 商品價格
- 評論數量
- 商品網址

pandas 負責：

- 移除價格符號
- 將價格轉成數字
- 移除重複商品
- 依價格排序
- 計算平均價格
- 儲存 CSV
