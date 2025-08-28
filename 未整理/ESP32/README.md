## 1. ESP32 接腳圖

![upgit_20250107_1736232321.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250107_1736232321.png)

## 2. ESP32 LODIN D32 連接 wifi

-   ESP32 不支援 5G 網路，只能吃 2.4G 的

```py
import network
import time

class CFG:
    # WiFi設定
    WIFI_SSID = "ALHC-guest"
    WIFI_PASSWORD = "ALHCguest"

# 初始化STA模式
sta = network.WLAN(network.STA_IF)
# network.STA_IF -> 工作站(類似行動裝置)
# network.AP_IF -> 熱點

sta.active(True) # 啟用STA接口
sta.connect(CFG.WIFI_SSID, CFG.WIFI_PASSWORD) # 嘗試連接WiFi
print("Connecting to WiFi...") # 檢查是否連線成功
start_time = time.time()
while not sta.isconnected():
    # 10秒超時
    if time.time() - start_time > 10:
        print("Failed to connect to WiFi")
        break
    pass

if sta.isconnected():
    print("Network config:", sta.ifconfig())
else:
    print("Could not connect to WiFi.")
```

## 3. Project：使用 ESP32 LODIN D32 發送郵件

![upgit_20241231_1735625527.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241231_1735625527.png)

![upgit_20241231_1735626224.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241231_1735626224.png)

-   [mail_ESP32_LODIND32](./mail_ESP32_LODIND32/main.py)

## 4. 物聯網雲端平台--ThinkSpeak

-   [main.py](./ESP32%20to%20thinkspeak/main.py)

![upgit_20250103_1735887073.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250103_1735887073.png)
![upgit_20250103_1735886923.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250103_1735886923.png)

## 5. 物聯網雲端平台--adafruit.io

-   https://io.adafruit.com/k3331363/dashboards/esp32-ce-shi-adafruit

![upgit_20250103_1735889416.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250103_1735889416.png)

## 6. MQTT

## 7. MQTT

-   MQTT(Message Queuing Telemetry Transport)是 OASIS 標準的一種訊息通訊協定(Message Protocol),這是架構在 TCP/IP 通訊協定
-   針對機器對機器(Machine-to-machine,M2M)的輕量級通訊協定。

![upgit_20250103_1735889491.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250103_1735889491.png)

### 7.1. MQTT 訊息

-   MQTT 訊息包含標頭(2 個字元)、訊息主題(Topic)和訊息內容(Payload)。
-   標頭可以指定：
    -   保留(Retained)訊息：當重新連接後，會保留上一次的最後訊息
    -   服務品質(Quality of Service,QoS)：
        -   0：最多傳送一次(at most once)：平信
        -   1：至少傳送一次(at least once)：掛號
        -   2：確實傳送一次(exactly once)：附回信

### 7.2. MQTT 主題

-   `主題等級/主題等級/主題`
-   MQTT 主題支持使用萬用字元來同時訂閱多個主題。

#### 7.2.1. 單層萬用字元 (Single Level Wildcard)

-   符號：`+`
-   功能：用來替代單層的主題等級。
-   範例：`home/sensor/+/temp`可以同時訂閱以下主題：
    -   `home/sensor/livingroom/temp`
    -   `home/sensor/kitchen/temp`
    -   `home/sensor/restroom/temp`

#### 7.2.2. 多層萬用字元 (Multi-level Wildcard)

-   符號：`#`
-   功能：用來替代多層的主題等級。
-   範例：`home/sensor/#`可以同時訂閱以下主題：
    -   `home/sensor/livingroom/temp`
    -   `home/sensor/kitchen/temp`
    -   `home/sensor/kitchen/brightness`
    -   `home/sensor/firstfloor/livingroom/temp`

### 7.3. MQTT 代理人 (MQTT Broker)

-   接收訊息：負責接收所有發布者的訊息。
-   過濾訊息：決定哪些訂閱者應接收哪些訊息。
-   傳送訊息：將消息發送至所有訂閱該主題的訂閱者。

#### 7.3.1. 公開 MQTT 代理人

-   HiveMQ MQTT
    -   主機名稱：broker.hivemq.com
    -   TCP 埠號：1883
    -   Websocket 埠號：8000
-   Eclipse IoT
    -   主機名稱：mqtt.eclipseprojects.io
    -   TCP 埠號：1883
    -   Websocket 埠號：8883
-   test.mosquitto.org
    -   主機名稱：test.mosquitto.org
    -   TCP 埠號：1883
    -   Websocket 埠號：8080
-   EMQX
    -   主機名稱：broker.emqx.io
    -   TCP 埠號：1883
    -   Websocket 埠號：8083

### 7.4. MQTT 客戶端

-   發送主題：test/topic

#### 7.4.1. 使用 powershell 發送

-   要先安裝[Download | Eclipse Mosquitto](https://mosquitto.org/download/)
-   將安裝位置加入路徑
-   發送消息：mosquitto_pub -h broker.hivemq.com -p 1883 -t "test/topic" -m "Hello MQTT"
-   監聽消息：mosquitto_sub -h broker.hivemq.com -p 1883 -t "test/topic"

#### 7.4.2. 使用 MQTT explorer 發送

-   選擇上述其中一個公開 MQTT 代理人，填入 TCP 跟 port
-   要到 advance 增加要監聽的主題

![upgit_20250103_1735891910.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250103_1735891910.png)

![upgit_20250103_1735891962.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250103_1735891962.png)

## 8. ESP32 LODIN D32 利用 MQTT 傳送感測器數據

```py
from umqtt.simple import MQTTClient
import network
import time

# WiFi配置
SSID ="ALHC-guest"
PASSWORD ="ALHCguest"


# MQTT配置
BROKER = "broker.hivemq.com"  # 公開 MQTT 代理人
TOPIC = "sensor/data"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Connected to WiFi:", wlan.ifconfig())

def send_data():
    client = MQTTClient("esp32", BROKER)
    client.connect()
    print("Connected to MQTT Broker")
    while True:
        data = "Hello from ESP32PPPPPPP"
        client.publish(TOPIC, data)
        print("Data sent:", data)
        time.sleep(1)

connect_wifi()
send_data()
```

## 9. python\*AI 生醫大感測

### 9.1. 膚電反應--GSR

-   膚電反應是一種基於皮膚電阻或電導變化的生理反應測量技術，常用於情緒、壓力和心理狀態的分析

-   交感神經系統的影響：
    -   當人類感到緊張、焦慮或說謊時，交感神經系統被激活。
    -   交感神經會引發身體的應激反應，例如心跳加速、血管收縮和汗腺分泌增加。
-   汗腺分泌與皮膚導電性：

    -   汗液含有電解質（如鈉、鉀離子），具有良好的導電性。
    -   汗液增多會導致皮膚表面的電阻降低或電導增加。

-   GSR 測量的技術原理
    -   皮膚電阻 (Skin Resistance)：通常皮膚的電阻值很高，但當汗液分泌增多時，電阻會顯著降低。
    -   皮膚電導 (Skin Conductance)：電導與電阻是反比關係，當皮膚電導增加時，電阻降低。
-   GSR 的應用
    -   測量用戶在特定情況下的情緒反應，如壓力、焦慮、恐懼或放鬆狀態。
    -   說謊檢測：皮膚電阻降低時，可能表示用戶感到緊張或說謊
    -   壓力監測與心理健康：用於心理研究和壓力管理，幫助追蹤壓力水平的變化。
    -   遊戲或娛樂體驗：實時測量玩家情緒，動態調整遊戲場景或難度。
-   數據讀取：
    -   ESP32 的 ADC (Analog-to-Digital Converter) 轉換模擬信號為數位數據，便於進一步處理與分析。

#### 9.1.1. 土壤濕度感測器的應用

![image|750](https://cdn.discordapp.com/attachments/1286741860538122281/1326128953165086801/IMG_8836.jpg?ex=677e4d54&is=677cfbd4&hm=688b23bcca18d9e4ad3fe534da15bc1d66b26f389223bb61ff9de7ee824a2bb4&)

-   感測器通過測量電壓變化來反映濕度狀況，類似於測量皮膚電阻的原理。
-   ESP32 開發板可將模擬電壓信號轉換為數位信號，便於後續數據分析與處理。

#### 接線方式：壤濕度感測器的連接

-   VCC → 3V
-   GND → GND
-   A0(信號腳) → GPIO36

#### 9.1.2. ESP32 的 ADC 設定：

-   土壤溫溼度的類比輸出腳位，連接到 ESP32 類比輸入角為，在使用 ADC 類別，變能測量電壓，得知電阻變化
-   atten (衰減量)：用於調整輸入電壓範圍。
    -   ADC.ATTN_0DB：100mV ~ 950mV
    -   ADC.ATTN_2_5DB：100mV ~ 1250mV
    -   ADC.ATTN_6DB：150mV ~ 1750mV
    -   ADC.ATTN_11DB：150mV ~ 2450mV
-   width (位元數)：用於調整 ADC 的取樣位元，位元數越高，解析度越高，數據越精細。
    -   ADC.WIDTH_9BIT： 9 位元 (0 ~ 511)
    -   ADC.WIDTH_10BIT：10 位元 (0 ~ 1023)
    -   ADC.WIDTH_11BIT：11 位元 (0 ~ 2047)
    -   ADC.WIDTH_12BIT：12 位元 (0 ~ 4095)
-   gsr 值越大，表示電阻越大，表示說謊可能性小

#### 程式碼

-   [ESP32 with 土壤感測器](./ESP32%20with%20土壤感測器/gsr.py)

### 10. 血氧濃度

-   氧氣從肺部吸入後，就會藉由血液運送至全身上下
-   血氧顧名思義就是氧氣佔血液中的比例。
-   血氧飽和度又可以分為：
    -   SaO2：以動脈血液進行分析，正常值為 97-100%
    -   SpO2：利用儀器取得周邊血管內的血氧飽和度，正常值需要大於 94%
    -   數值正常代表肺部交換氧氣功能沒問題，也代表心臟有能力含氧血運送到身體組織

#### 如何測量 SpO2

-   通常採用非入侵式且連續測量的方式。
-   利用缺氧血紅素與氧合血紅素對不同的光波長有不同吸收與反射率來達成
    -   缺氧血紅素：紅光吸收較多，紅外光吸收較少
    -   氧合血紅素：紅光吸收較少，紅外光吸收較多

#### 接線方式：壤濕度感測器的連接

-   VCC → 3V
-   GND → GND
-   SCL → 22(SCL)
-   SDA → 21(SDA)

#### 程式碼

-   [ppg.py](./ESP32%20with%20MAX30102/ppg.py)

![upgit_20250109_1736421977.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250109_1736421977.png)

![image](https://cdn.discordapp.com/attachments/1286741860538122281/1326429217415761960/IMG_8837.jpg?ex=677f64f9&is=677e1379&hm=4293cedb1939848bbccf9e74b2e2748b3132531c7abc0fd52dea42d21607dad0&)

## 11. 利用 PPG 值檢測心率

-   心率 = 1/時間週期(兩個波之間)
-   不同人/不同環境測到的 PPG 不同，進而計算心率的值也會有所差異
-   設定動態閥值
-   [ppg_pulse_rate.py](./ESP32%20with%20MAX30102/ppg_pulse_rate.py)

## 心電訊號(ECG)

-   心臟跳動是因為心肌受到動作電位而產生收縮，而動作電位會散步到全身，引發一連串微小電學變化。
-   我們可以藉由電極貼片與感測器來捕捉並放大訊號，這些訊號一時間呈現即為心電圖(Electrocardiogram, ECG)
-   一個心臟週期可以分為 P、Q、R、S、T 波

![upgit_20250110_1736489517.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250110_1736489517.png)

### 測量心電圖

-   量測心電圖時，需要以電極貼片貼於皮膚表面，透過兩個以上的電極貼片來取得不同點的電位差。
-   不同位置所記錄的電位波行稱為 導程 ，可分為
    -   胸導程：醫院通常使用
    -   肢體導程：較方便，本次所使用，稱為艾因斯托三角。

![upgit_20250110_1736489969.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250110_1736489969.png)

### 感測器

-   使用 AD8232，該感測器內建類比率波器與放大器，可以捕捉皮膚上的微小 EGG 訊號並放大。
-   電極貼片
    -   黃色 => 左手
    -   紅色 => 右手
    -   綠色 => 左腳

![image](https://media.discordapp.net/attachments/1286741860538122281/1327160668092235776/IMG_8849.jpg?ex=67820e30&is=6780bcb0&hm=c2a43d6fe59b1f7c9a07e8875059aaf92b3dbfb67efcb5c045b0c5cf2377aca4&=&format=webp&width=604&height=453)

![image](https://cdn.discordapp.com/attachments/1286741860538122281/1327160668809592832/IMG_8850.jpg?ex=67820e30&is=6780bcb0&hm=24c46a9e652226380c08db63eefaa518c641dd6c6f395c86359b9cd4e4678244&)

#### 接線方式

-   3.3V => 3V
-   GND => GND
-   OUTPUT => VP

#### 程式碼

-   [取出 ECG 值](./ESP32%20with%20AD8232/ecg.py)
-   [利用 ECG 值換算心率(失敗率蠻高)](./ESP32%20with%20AD8232/ecg_pulse.py)

## 呼吸訊號 RSP

-   正常人一分鐘呼吸 12-20 次(呼吸頻率)，而使用感測器測量呼吸深淺變化，即為呼吸訊號(resporation, RSP)

### 測量方式

-   這邊使用的方式為溫度變化法，由於人體溫度恆為 37，會與室溫產生溫差，因此只要測量口鼻附近的氣溫變化，就能取得 RSP 訊號。
-   我們使用 NTC 熱敏電阻
    -   當溫度降低時，他的電阻值就會提升
    -   在利用分壓電路取得電壓變化變轉換為 RSP 訊號。

### 程式碼

-   [測出 rsp 值](./ESP32%20with%20NTC熱敏電阻/rsp.py)
-   [rsp 值換算呼吸頻率](./ESP32%20with%20NTC熱敏電阻/breathe_rsp.py)
