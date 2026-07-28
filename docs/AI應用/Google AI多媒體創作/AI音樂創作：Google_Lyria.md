# AI音樂與情緒設計：Lyria音樂創作

> 前面的 AI 創作流程，常常把焦點放在「畫面能不能被看見」。但完整作品不只要被看見，也要被感受。畫面告訴觀眾發生了什麼，聲音則告訴觀眾應該怎麼感受。  
> 同一個人走在街上，沒有音樂時只是普通畫面；搭配溫暖音樂，可能像生活感或療癒故事；搭配緊張音樂，立刻像懸疑片。聲音不是最後才補上的裝飾，而是創作一開始就該決定的情緒核心。

### 聲音如何改變觀眾感受

觀眾接收影片時，通常先被聲音的節奏與氛圍影響，再理解畫面內容。

- 緩慢的鋼琴：溫柔、感性、回憶、療癒
- 強烈的節奏音樂：緊張、速度、推進、行動
- 安靜或環境聲：真實、沉浸、孤獨、留白
- 漸強音樂：即將發生重要事件
- 突然中斷：轉折、驚訝、危機
- 持續堆疊：期待與故事張力

### 聲音如何讓畫面產生敘事

單一畫面只是瞬間，聲音可以把瞬間變成過程：

- 音樂漸強 → 觀眾預期事件即將發生。
- 節奏突然中斷 → 製造轉折或驚喜。
- 情緒逐步堆疊 → 建立故事張力。

因此，沒有聲音的畫面，是片段；有聲音的畫面，才可能成為故事。

### 聲音建立記憶點

人們記住作品，常常不是只記得畫面，而是記得整體感受，而感受很大一部分來自聲音。

- 某段旋律讓人立刻想到某支影片。
- 某種音樂風格代表某個品牌。
- 某種聲音氛圍產生情緒連結。

聲音不只是輔助，而是作品被記住的關鍵。

### 沒有音樂的作品為什麼不完整

沒有音樂時，觀眾仍能理解場景、動作與角色，但通常只能停在「資訊層」：

- 畫面顯得平淡。
- 轉場缺乏張力。
- 情緒無法累積。
- 節奏不容易被感知。
- 作品難以被記住。

小結：

- 畫面讓人理解內容。
- 聲音讓人產生感受。
- 兩者結合，創作才真正完整。

## Lyria 是什麼：從「使用音樂」到「創作音樂」

- [Google Lyria](https://deepmind.google/models/lyria/)
- [Suno](https://suno.com)

### 音樂生成的三個核心元素

1. 情緒(Emotion)。決定整體氛圍，是最重要的起點。

```text
- 溫暖：warm, cozy
- 緊張：tense, suspenseful
- 希望：hopeful, uplifting
- 好奇：curious
- 動感：energetic, playful
- 孤獨：lonely, reflective
```

2. 節奏(Rhythm／Tempo)。決定速度與推進感，也會直接改變影片觀看感受。

```text
- 慢節奏：敘事、感性、鋪陳
- 中節奏：日常、穩定、一般內容推進
- 快節奏：動作、轉折、緊張
- 動態節奏：配合情緒曲線與鏡頭變化
```

3. (風格 Style)。決定聲音的質感與類型。

```text
- 電影感 cinematic
- 鋼琴 piano-based
- 電子 electronic
- 放鬆氛圍 lo-fi
- 管弦樂 orchestral
- 卡通感 cartoon style
```

## 從文字生成音樂（Text → Music）

### Music 與 Song 的差別

- Music：用來支持畫面、建立情緒與氛圍，通常是無人聲背景音樂。
- Song：本身可以成為內容主體，以歌詞強化訊息與表達。

兩者不是風格差異，而是用途差異。

關鍵詞教學：

```text
### 明確要求背景音樂。
- `instrumental`(樂器演奏)
- `no vocals`(無人聲)
- `background music only`
```

```text
### 明確要求歌曲與歌詞主題。
- `song`
- `with lyrics`
- `lyrics about...`
```

### Prompt 基本結構

四個核心元素：「主題 Theme × 情緒 Emotion × 節奏 Tempo × 風格 Style」

```text
### 建議流程：

1. 先以中文想清楚需求。
2. 再轉成簡潔英文生成提示。
3. 明確寫出是否需要人聲。

# 中文幫助釐清情緒與方向；英文通常有助於提高生成描述的精確度。若平台支援中文，也可直接使用中文，比較兩種結果。
```

### Problem. 溫暖敘事（完整保留）

```text
### 背景音樂 Music｜無人聲版

### 中文理解：
溫暖、慢節奏、以鋼琴為主、具有電影感的背景音樂，適合故事影片，無人聲。

### 生成用 Prompt：
Warm, slow-tempo, piano-based cinematic instrumental background music for a heartfelt story. Gentle emotional development, subtle strings, no vocals, background music only.

### 關鍵詞：`instrumental`、`no vocals`、`background music only`
```

<!-- 播放影片 -->
<div class="video-wrapper">
    <iframe
        src="https://drive.google.com/file/d/1x_OVu8cHuDQ2WgZTjT4E92QdkKXt9K1k/preview" 
        allow="autoplay"
        allowfullscreen>
    </iframe>
</div>

```text
### 歌曲 Song｜含人聲版

### 中文理解：
一首溫暖、慢節奏的鋼琴歌曲，具有電影感，歌詞描述生活中的小確幸與希望。

### 生成用 Prompt：
A warm, slow-tempo piano song with a cinematic style, with lyrics about small moments of happiness, hope, and finding light in everyday life.
```

<div class="video-wrapper">
    <iframe
        src="https://drive.google.com/file/d/1OUCuRJVF6AwIkwABpUwrwMqTch8gG35I/preview" 
        allow="autoplay"
        allowfullscreen>
    </iframe>
</div>

### Problem. EDM 風格

```text
### 背景音樂 Music｜無人聲版

### 中文理解：
一首充滿能量的 EDM 電子舞曲，節奏明快，具有未來科技感，適合作為科技產品展示影片背景音樂，無人聲。

### 生成用 Prompt：
Energetic EDM background music with a futuristic atmosphere, fast tempo, powerful electronic beats, deep bass, uplifting synths, cinematic build-ups and drops, instrumental, no vocals, perfect for a technology product showcase.
```

<div class="video-wrapper">
    <iframe
        src="https://drive.google.com/file/d/1iJ6Ap-IviMj-GVrapAAx9kqdmbw0a8V8/preview" 
        allow="autoplay"
        allowfullscreen>
    </iframe>
</div>

```text
### 背景音樂 Music｜含人聲版

### 中文理解：
一首充滿未來感的 EDM 歌曲，節奏快速且充滿能量，歌詞描述科技如何改變世界、創新以及人類的無限可能。

### 生成用 Prompt：
An energetic EDM song with a futuristic atmosphere, fast tempo, powerful drops, uplifting electronic synths, and lyrics about technology transforming the world, innovation, and limitless human potential.
```

<div class="video-wrapper">
    <iframe
        src="https://drive.google.com/file/d/1QPzRYHTZCwl6s3396B7aQrhLWKrmi7_S/preview" 
        allow="autoplay"
        allowfullscreen>
    </iframe>
</div>

### Problem. 咖啡廳情境（溫暖氛圍）

```text
### 歌曲 Song｜無人聲版

### 中文理解：
溫暖、輕鬆、中慢節奏、Lo-fi 風格背景音樂，適合咖啡廳氛圍，無人聲。

### 生成用 Prompt：
Warm, relaxed, medium-slow tempo lo-fi ambient background music for a cozy café. Soft beat, mellow keys, instrumental, no vocals.
```

<div class="video-wrapper">
    <iframe
        src="https://drive.google.com/file/d/1JDpRv0Ie2gckuyQQJG3yMp0eWkftbU2z/preview" 
        allow="autoplay"
        allowfullscreen>
    </iframe>
</div>

```text
### 歌曲 Song｜含人聲版

### 中文理解：
一首溫暖、輕鬆的 Lo-fi 歌曲，中慢節奏，歌詞描述咖啡與日常生活。

### 生成用 Prompt：
A warm and relaxed lo-fi song, medium-slow tempo, with lyrics about coffee, quiet mornings, and small moments in daily life.
```

<div class="video-wrapper">
    <iframe
        src="https://drive.google.com/file/d/1XRz5TwoNXOcguaHoGAEUo8NPJ4Hx9ZpB/preview" 
        allow="autoplay"
        allowfullscreen>
    </iframe>
</div>

## 從圖像生成音樂（Image → Music）

轉換邏輯：「畫面 → 情緒判讀 → 節奏推測 → 風格選擇 → 音樂 Prompt」

圖像不只提供物件，也提供情緒訊號。分析圖片時，可觀察三個層面：

```text
### 光線 Lighting

- 柔和光線 → 溫暖、放鬆
- 強烈對比 → 緊張、戲劇感
- 昏暗光線 → 神秘、壓迫、懸疑
```

```text
### 色調 Color Tone

- 暖色系（橙、黃）→ 溫馨、舒適
- 冷色系（藍、紫）→ 冷靜、科技感
- 高對比色 → 活潑、強烈、速度感
```

```text
### 場景與內容 Scene & Subject

- 咖啡廳 → 輕鬆、日常
- 未來城市 → 科技、節奏感
- 空曠場景 → 孤獨、沉靜
```

### Problem. 同一角色 × 三種場景

設定同一隻熊貓外送員，保持外觀一致，只改變場景與音樂。

場景一：悠閒小鎮(輕鬆日常)
![](./Image/Google%20Lyria/熊貓外送員騎著腳踏車.png)

```text
### 圖片內容：
熊貓外送員騎著腳踏車，穿梭在陽光灑落的小鎮街道，準備配送餐點。
(無提示詞先生成一次，觀察 AI 對圖片的直覺判讀。)

### 背景音樂 Prompt：
Warm, relaxed lo-fi background music, medium-slow tempo, soft acoustic guitar and gentle piano, cozy neighborhood atmosphere, instrumental, no vocals.

### 歌曲 Prompt：
A warm and relaxed lo-fi song, medium-slow tempo, with lyrics about delivering happiness, friendly neighborhoods, and enjoying everyday life.
```

場景二：雨天城市(專注與努力)
![](./Image/Google%20Lyria/熊貓外送員穿著雨衣.png)

```text
### 圖片內容：
同一隻熊貓外送員穿著雨衣，在下雨的城市中努力送餐。
(無提示詞先生成一次，觀察 AI 對圖片的直覺判讀。)

### 背景音樂 Prompt：
Focused ambient background music, medium tempo, soft piano, subtle electronic textures, determined and steady mood, instrumental, no vocals.

### 歌曲 Prompt：
A motivational pop song, medium tempo, with lyrics about perseverance, responsibility, and never giving up despite the rain.
```

場景三：未來都市(科技與速度)

![](./Image/Google%20Lyria/熊貓外送員騎著懸浮機車.png)

```text
### 圖片內容：
同一隻熊貓外送員騎著懸浮機車，穿梭在霓虹閃爍的未來城市，高樓林立，充滿科技感。
(無提示詞先生成一次，觀察 AI 對圖片的直覺判讀。)

### 背景音樂 Prompt：
Futuristic electronic background music, medium-fast tempo, cinematic electronic score, energetic pulse, modern synth textures, instrumental, no vocals.

### 歌曲 Prompt：
A futuristic electronic song, medium-fast tempo, with lyrics about speed, innovation, smart cities, and delivering to the future.
```

## 音樂風格、情緒控制與一致性

### 常見音樂風格

```text
1. 電影感 Cinematic
   特點：情緒強、層次分明。
   適合：故事影片、品牌影片。

2. 輕鬆氛圍 Lo-fi
   特點：放鬆、日常、低干擾。
   適合：生活影片、咖啡廳情境。

3. 電子音樂 Electronic
   特點：節奏強、科技感。
   適合：未來場景、科技產品。

4. 管弦樂 Orchestral
   特點：戲劇性、層次豐富。
   適合：動畫角色、故事高潮。
```

### 情緒控制三大元素

公式：「節奏 × 音色 × 強弱 = 情緒控制」

```text
### 節奏 Tempo

- slow → 平靜、敘事
- medium → 穩定、日常
- fast → 緊張、動作
```

```text
### 音色 Tone／Instrument

- 鋼琴 → 溫暖、情感
- 電子 → 科技、未來
- 弦樂 → 劇情、張力
```

```text
### 強弱 Intensity

- 柔和 → 放鬆
- 漸強 → 推進
- 高峰 → 爆發
```

### Problem. 溫馨回憶影片

「製作一段家庭相簿影片的背景音樂，希望聽起來溫暖、放鬆，像是在回憶美好的時光，不要有人聲。」

請依據情境寫出Music Prompt，並利用寫出的Music Prompt做出Music。

```text
- 風格(Style)：
- 節奏(Tempo)：
- 音色(Tone / Instrument)：
- 情緒(Mood)：
- 強弱(Intensity)：
- 人聲(Vocals)：
```

### Problem. 科技產品發表

「製作一支 AI 智慧眼鏡的產品介紹影片，希望充滿科技感，節奏明快，能展現未來世界的氛圍，無人聲。」

請依據情境寫出Music Prompt，並利用寫出的Music Prompt做出Music。

```text
- 風格(Style)：
- 節奏(Tempo)：
- 音色(Tone / Instrument)：
- 情緒(Mood)：
- 強弱(Intensity)：
- 人聲(Vocals)：
```

### Problem. 奇幻冒險

「製作一位勇者踏入古老神殿，即將展開冒險。希望音樂具有史詩感，情緒逐漸堆疊，最後進入高潮，無人聲。」

請依據情境寫出Music Prompt，並利用寫出的Music Prompt做出Music。

```text
- 風格(Style)：
- 節奏(Tempo)：
- 音色(Tone / Instrument)：
- 情緒(Mood)：
- 強弱(Intensity)：
- 人聲(Vocals)：
```

### Problem. 極速賽車

「製作賽車高速衝刺、超車、最後衝過終點，希望音樂充滿速度感與緊張感，情緒一路推向最高點。」

請依據情境寫出Music Prompt，並利用寫出的Music Prompt做出Music。

```text
- 風格(Style)：
- 節奏(Tempo)：
- 音色(Tone / Instrument)：
- 情緒(Mood)：
- 強弱(Intensity)：
- 人聲(Vocals)：
```

### Problem. 星空縮時攝影

「夜晚星空慢慢移動，銀河緩緩升起，希望音樂空靈、夢幻，帶有神秘感，無人聲。」

請依據情境寫出Music Prompt，並利用寫出的Music Prompt做出Music。

```text
- 風格(Style)：
- 節奏(Tempo)：
- 音色(Tone / Instrument)：
- 情緒(Mood)：
- 強弱(Intensity)：
- 人聲(Vocals)：
```

### Problem. 懸疑推理

「偵探走進昏暗的房間尋找線索，希望音樂能營造神秘與緊張感，但不要太激烈，慢慢增加壓迫感。」

請依據情境寫出Music Prompt，並利用寫出的Music Prompt做出Music。

```text
- 風格(Style)：
- 節奏(Tempo)：
- 音色(Tone / Instrument)：
- 情緒(Mood)：
- 強弱(Intensity)：
- 人聲(Vocals)：
```

### Problem. 運動品牌廣告

「運動員清晨訓練、奔跑、跳躍，最後完成挑戰，希望音樂充滿力量與激勵感。」

請依據情境寫出Music Prompt，並利用寫出的Music Prompt做出Music。

```text
- 風格(Style)：
- 節奏(Tempo)：
- 音色(Tone / Instrument)：
- 情緒(Mood)：
- 強弱(Intensity)：
- 人聲(Vocals)：
```
