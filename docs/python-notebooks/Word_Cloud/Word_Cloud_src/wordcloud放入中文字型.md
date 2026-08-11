```py
from wordcloud import WordCloud
from PIL import Image

font_path = "../Word_Cloud_assets/NotoSansTC-VariableFont_wght.ttf" # 中文字型檔

lyrics = """
我拼了命的隱藏著痛
努力微笑想讓你回頭
被淚水打濕的是一場夢
我在掩飾我的執著
愛還會不會回來
這是我的獨白
"""

# 產生文字雲的核心城市碼
wd = WordCloud(font_path=font_path).generate(lyrics)
imageCloud = wd.to_image()       # 由WordCloud物件建立詞雲影像檔


### 處理圖片輸出
# img_resized = imageCloud.resize((300, 200)) # 調整大小
imageCloud.show()
```
