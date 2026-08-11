```py
# 歌詞->統計數量->詞頻->詞雲->作圖出來顯示給你看
from wordcloud import WordCloud

# python 開啟檔案的指令
with open("../Word_Cloud_assets/素材：英文歌詞.txt") as fp:  # 英文字的文字檔
    text = fp.read()              # 讀取檔案

# 產生文字雲的核心城市碼
wd = WordCloud().generate(text)   # 由txt文字產生WordCloud物件
imageCloud = wd.to_image()       # 由WordCloud物件建立詞雲影像檔


### 處理圖片輸出
# img_resized = imageCloud.resize((300, 200)) # 調整大小
imageCloud.show()
```
