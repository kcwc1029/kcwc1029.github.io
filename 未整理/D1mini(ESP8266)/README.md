## 3. D1 mini 接腳圖

![upgit_20241227_1735277114.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241227_1735277114.png)

### 有 11 個數位 IO 腳位，支持以下功能：

-   GPIO0 (D3): 可作為數位 IO 或其他功能腳位。
-   GPIO1 (TX): 用於 UART 傳輸數據，也可作為數位 IO。
-   GPIO2 (D4): 默認接上內部 LED，支持數位 IO。
-   GPIO3 (RX): 用於 UART 接收數據，也可作為數位 IO。
-   GPIO4 (D2): 通用數位 IO 腳位。
-   GPIO5 (D1): 通用數位 IO 腳位。
-   GPIO12 (D6): 通用數位 IO 腳位。
-   GPIO13 (D7): 通用數位 IO 腳位。
-   GPIO14 (D5): 通用數位 IO 腳位。
-   GPIO15 (D8): 通用數位 IO 腳位，內部有下拉電阻。
-   GPIO16 (D0): 通用數位 IO 腳位，支持深度睡眠喚醒功能。
-   有一個類比輸入腳位：
    -   A0 (ADC)：可測量的電壓範圍：0 ~ 1.0V。

## 1. D1mini 安裝事項

-   插入電腦後，要到裝置管理員察看

![upgit_20241225_1735116720.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735116720.png)

-   要安裝 CH340 驅動程式：https://www.wch.cn/download/ch341ser_exe.html

## 2. 燒錄+使用

-   這邊花了窩一整天 QQ

### 2.1. 方式 1：使用 arduino 開發

-   一樣開 arduino IDE
-   在偏好設定添加 ESP8266 的開發版管理員網址：http://arduino.esp8266.com/stable/package_esp8266com_index.json
-   在【開發版管理員】安裝【esp8266】
    ![upgit_20241225_1735127961.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735127961.png)

-   板子記得要選好，不然會燒不進去
    ![upgit_20241225_1735127992.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735127992.png)

-   測試程式碼

```cpp
// TODO: 測試控制Ｄ1mini內建LED

void setup() {
pinMode(LED_BUILTIN, OUTPUT); // 設置內建 LED (GPIO2) 為輸出
}

void loop() {
digitalWrite(LED_BUILTIN, LOW);  // 開啟 LED
delay(1000);                    // 延遲 1 秒
digitalWrite(LED_BUILTIN, HIGH); // 關閉 LED
delay(1000);                    // 延遲 1 秒
}
```

### 2.2. 方式 2：使用 micropython 開發(有兩種燒錄方式)

#### 2.2.1. 第一種：thonny 內建燒錄(2024.12.25 使用失敗)

![upgit_20241225_1735128135.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735128135.png)

![upgit_20241225_1735128158.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735128158.png)

![upgit_20241225_1735128185.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735128185.png)

#### 2.2.2. 第 2 種：NodeMCU pyflasher 燒錄(有成功)

-   先去下載韌體：[MicroPython - Python for microcontrollers](https://micropython.org/download/ESP8266_GENERIC/)
-   下載燒入軟體：[Release 5.0 - bumping dependencies · marcelstoer/nodemcu-pyflasher](https://github.com/marcelstoer/nodemcu-pyflasher/releases/tag/v5.0.0)
-   那個 exe 把他載下來
    ![upgit_20241225_1735128522.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735128522.png)

### 2.3. 燒錄完後，執行程式看看

```python
# TODO: 查看是否能透過micropython操作

from machine import Pin
import utime

led = Pin(2, Pin.OUT)
while True:
    led.value(0)
    utime.sleep(1)
    led.value(1)
    utime.sleep(1)
```

-   儲存在本地端即可
    ![upgit_20241225_1735128660.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241225_1735128660.png)

## 4. 數位腳位輸入/輸出

-   [控制 LED 亮暗](./digital%20input%20output/LED_Blink.py)

-   [讀取腳位狀態值來閃爍 LED](./digital%20input%20output/LED_Status_Change.py)

## 5. 類比輸入/輸出

-   [PWM01](./analog%20input%20output/PWM01.py)
-   [PWM02](./analog%20input%20output/PWM02.py)
-   [3 色 LED 數位輸出：開關按一下亮紅 LED，按一下亮綠 LED，按一下亮藍 LED](./analog%20input%20output/ThreeColorLED_ButtonToggle.py)

-   [類比輸入：以光敏電阻為例](./analog%20input%20output/Photoresistor_Analog.py)

-   [光敏電阻控制 LED](./analog%20input%20output/Photoresistor_LED.py)

-   [實作全彩 RGB LED](./analog%20input%20output/RGB_LED.py)

## 6. D1mini 連接 wifi 基地台

-   D1mini 雖然可以連接網路，但硬體設備過小，其實很多事也無法做。
-   STA 模式(station)：讓 ESP8266 如同一張 widi 無線網路卡，可以連線至可用基地台
-   AP 模式(access point)：讓 ESP8266 作為熱點

-   [顯示可連線 wifi 基地台的 mac 地址](./wifi/D1mini_Show_IP.py)

-   [在成功連線 WiFi 基地台後馬上中斷連線](./wifi/D1mini_Wifi_Disconnect.py)

## 10. Project：程式模組化並連線到 wifi

-   要將連線 widi 帳密輸入至 config.py
-   [module_connect_wifi](./module_connect_wifi/connect_wifi.py)
