## HW要求

目標網站：https://www.scrapethissite.com/pages/ajax-javascript/

網站只有在使用者點擊年份後，才透過 AJAX 載入該年度的奧斯卡電影資料。請使用 Selenium 自動點擊年份並擷取結果。

請完成以下流程：

```
等待年份按鈕
→ 保存目前的舊資料
→ 點擊指定年份
→ 等待 Loading 消失
→ 等待舊資料 stale
→ 重新取得電影資料
```

擷取：

- 年份
- 電影名稱
- 提名數量
- 得獎數量
- 是否獲得最佳影片

請至少處理三個年份，並合併成同一份 DataFrame。
