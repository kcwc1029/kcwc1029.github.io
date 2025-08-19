from wordcloud import WordCloud




with open("./Eenie Meenie歌詞.txt") as fp:  # 英文字的文字檔
    text = fp.read()              # 讀取檔案

wd = WordCloud().generate(text)   # 由txt文字產生WordCloud物件
imageCloud = wd.to_image()       # 由WordCloud物件建立詞雲影像檔
imageCloud.show()                # 顯示詞雲影像檔