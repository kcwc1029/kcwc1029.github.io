```py
from wordcloud import WordCloud
import jieba

text = """
從不主動示弱
我們的過去
分分合合太多
傷人的話難說
卻覺得很灑脫
曾經的那些發生過的開心和難過
就像開敗的花
浪也拍打著沙
我卻對你情有獨鍾
我陪你留下
說最浪漫的話
即便是青春的懵懂
但是我們漸行漸遠
逐漸帶上現實的枷鎖
信任在短短解釋後崩塌
"""

# 中文斷詞
words_list = jieba.cut(text, cut_all=False)
text_processed = " ".join(words_list)
# print("偷看切好的樣子：", text_processed)

# 設定文字雲參數
wc = WordCloud(
    background_color='white',
    width=800,
    height=600,
    font_path = "../Word_Cloud_assets/NotoSansTC-VariableFont_wght.ttf", # 中文字型檔
    max_words=50
)

# 產生文字雲
wc.generate(text_processed)
imageCloud = wc.to_image()

### 處理圖片輸出
img_resized = imageCloud.resize((300, 200)) # 調整大小
img_resized.show()
```
