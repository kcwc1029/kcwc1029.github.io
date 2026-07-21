### list(字串)：把字串裡的每個字（包含標點符號）都拆成獨立元素。
news = "颱風過境"
news_list = list(news)
print(f"list() 拆解後：{news_list}") # ['颱', '風', '過', '境']

### split(分隔符號)：精準切割。根據你指定的符號把字串切開。如果不填，預設會用「空白」來切。
tags = "Python,Java,C++,Go"
tag_list = tags.split(",") # 以逗號為刀
print(f"split() 切割後：{tag_list}") # ['Python', 'Java', 'C++', 'Go']

### join(串列)：把串列中的每個字串串聯起來。注意：語法是 “膠水”.join(串列)。
words = ['Hello', 'World']
sentence = " ".join(words) # 用空格當膠水
print(f"join() 重組後：{sentence}") # "Hello World"