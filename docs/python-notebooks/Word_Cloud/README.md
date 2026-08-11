# Word_Cloud

==專案下載：https://github.com/kcwc1029/kcwc1029.github.io/tree/main/docs/python-notebooks/Gmail==

想像你讀了一本很厚的書，或是看了一萬則網路留言。如果要把這些文字變成一張圖，該怎麼做？

文字雲的原理很簡單：

- 統計出現次數： 算出這篇文章中，哪些詞出現最多次。
- 大小決定權重： 出現越多次的詞，字體就越大、越粗；出現越少的詞，字體就越小。
- 拼圖排列： 把這些大小不一的詞，像拼圖一樣塞在一起，形成一張圖。

## 安裝套件

```
!pip install wordcloud -q
```

## (回顧)長文字使用

```py
text = """
She's indecisive she can't decide
She keeps on looking from left to right
Girl come a bit closer look in my eyes
Searching is so wrong I'm Mr. Right
You seem like the type to love 'em and leave 'em
And disappear right after this song
So give me the night to show you hold you
Don't leave me out here dancin' alone
"""
```

## 英文詞雲

- [範例：將英文句子轉換為詞雲](./Word_Cloud_src/將英文句子轉換為詞雲.md)
- [範例：將英文放在txt，在轉化為詞雲](./Word_Cloud_src/將英文放在txt，在轉化為詞雲.md)

## 中文詞雲

![upgit_20260502_1777737552.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/05/upgit_20260502_1777737552.png)

### 第一種方式：因為wordcloud他本身並不具備中文字形，所以直接引入中文字型。

- [範例：wordcloud放入中文字型](./Word_Cloud_src/wordcloud放入中文字型.md)

### 第二種方式：將中文放轉化為文字雲，應用jebia

但這樣其實並不是沒有真正處裡到斷詞(Tokenization)：英文單字有用空白隔開 (e.g., Hello World)，但中文沒有(e.g., 你好世界)，所以要用工具把詞切開(e.g., 你好 / 世界)。

這邊我們會借用到 jieba 這個套件。

```shell
!pip install jieba -q
```

- [範例：應用jebia](./Word_Cloud_src/應用jebia.md)

### Problem.

透過for迴圈的方式，將歌詞：[一吻Remix](./Word_Cloud_assets/歌詞：一吻%20Remix.txt)、[不是故意](./Word_Cloud_assets/歌詞：不是故意.txt)、[海嶼你](./Word_Cloud_assets/歌詞：海嶼你.txt) 共三首歌詞讀擋轉文字雲
