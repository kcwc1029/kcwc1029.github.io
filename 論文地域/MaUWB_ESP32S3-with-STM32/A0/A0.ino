/*
  MaUWB_ESP32S3-with-STM32 Anchor 指令範例程式碼
  使用的函式庫版本:
  - Wire: 2.0.0
  - Adafruit_GFX_Library: 1.11.7
  - Adafruit_BusIO: 1.14.4
  - SPI: 2.0.0
  - Adafruit_SSD1306: 2.5.7
*/

// 使用者自定義設定區域 ------------------------------------------

#define UWB_INDEX 2  // 定義 UWB 裝置編號，這裡的數值可調整為不同裝置的 ID
#define ANCHOR      // 定義此裝置為「錨點」(Anchor)角色
#define FREQ_6800K  // 使用 6.8M 頻率
#define UWB_TAG_COUNT 64  // UWB 可支持的 Tag 數量，這裡可以依需求調整

// 使用者自定義設定結束 ------------------------------------------

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

#define SERIAL_LOG Serial       // 定義 LOG 使用的 Serial 通訊 (debug 用)
#define SERIAL_AT mySerial2     // 定義 AT 指令使用的 Serial 通訊 (與 STM32 通訊)

HardwareSerial SERIAL_AT(2);    // 初始化第二組硬體序列端口，對應到 UART2

// ESP32S3 I/O 定義
#define RESET 16   // RESET 腳位
#define IO_RXD2 18 // UART2 的 RXD
#define IO_TXD2 17 // UART2 的 TXD
#define I2C_SDA 39 // I2C 的 SDA 腳位
#define I2C_SCL 38 // I2C 的 SCL 腳位

Adafruit_SSD1306 display(128, 64, &Wire, -1);  // 初始化 SSD1306 顯示器

void setup() {
    pinMode(RESET, OUTPUT);       // 設置 RESET 腳位為輸出
    digitalWrite(RESET, HIGH);    // 將 RESET 設置為高電位，啟動裝置

    SERIAL_LOG.begin(115200);     // 初始化 Serial 日誌輸出 (用於 debug)
    SERIAL_LOG.print(F("Hello! ESP32-S3 AT command V1.0 Test"));

    // 初始化 SERIAL_AT 用於與 STM32 通訊，波特率設為 115200
    SERIAL_AT.begin(115200, SERIAL_8N1, IO_RXD2, IO_TXD2);

    SERIAL_AT.println("AT");     // 發送 AT 指令進行檢測
    Wire.begin(I2C_SDA, I2C_SCL); // 初始化 I2C
    delay(1000);                 // 延遲 1 秒等待初始化完成

    // 初始化 SSD1306 顯示器
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        SERIAL_LOG.println(F("SSD1306 allocation failed"));
        for (;;);
    }
    display.clearDisplay();      // 清除顯示內容

    logoshow();                  // 顯示 Logo 和初始化信息

    sendData("AT?", 2000, 1);       // 發送 AT 測試命令
    sendData("AT+RESTORE", 5000, 1); // 重置裝置設置

    sendData(config_cmd(), 2000, 1); // 發送配置信息
    sendData(cap_cmd(), 2000, 1);    // 發送容量設置命令

    sendData("AT+SETRPT=1", 2000, 1);  // 開啟報告模式
    sendData("AT+SAVE", 2000, 1);      // 保存設置
    sendData("AT+RESTART", 2000, 1);   // 重啟裝置
}

long int runtime = 0;
String response = "";            // 保存接收到的資料
String rec_head = "AT+RANGE";    // 定義接收到 AT 指令的前綴

void loop() {
    // 檢查 Serial 輸入
    while (SERIAL_LOG.available() > 0) {
        SERIAL_AT.write(SERIAL_LOG.read());
        yield();
    }

    // 檢查 AT 指令的回應
    while (SERIAL_AT.available() > 0) {
        char c = SERIAL_AT.read();
        if (c == '\r') continue;  // 忽略回車符號
        else if (c == '\n') {     // 當接收到換行時，輸出完整回應
            SERIAL_LOG.println(response);
            response = "";
        } else {
            response += c;        // 儲存每個接收到的字元
        }
    }
}

// 顯示 Logo 及初始化信息
void logoshow(void) {
    display.clearDisplay();
    display.setTextSize(1);             // 設置文字大小
    display.setTextColor(SSD1306_WHITE); // 設置文字顏色
    display.setCursor(0, 0);            // 設置文字起始位置
    display.println(F("MaUWB DW3000"));

    display.setCursor(0, 20);           // 設置第二行文字起始位置
    display.setTextSize(2);             // 調整文字大小

    String temp = "";
    temp = temp + "A" + UWB_INDEX;      // 顯示 UWB ID
    temp = temp + "   6.8M";            // 顯示頻率
    display.println(temp);

    display.setCursor(0, 40);           // 第三行顯示 UWB Tag 數量
    temp = "Total: ";
    temp = temp + UWB_TAG_COUNT;
    display.println(temp);

    display.display();                  // 顯示更新的內容
    delay(2000);                        // 延遲 2 秒
}

// 發送 AT 指令的通用函數
String sendData(String command, const int timeout, boolean debug) {
    String response = "";
    SERIAL_LOG.println(command);
    SERIAL_AT.println(command);  // 將指令發送給 STM32

    long int time = millis();
    while ((time + timeout) > millis()) {
        while (SERIAL_AT.available()) {
            char c = SERIAL_AT.read(); // 讀取回應字元
            response += c;
        }
    }

    if (debug) {
        SERIAL_LOG.println(response); // 如果 debug 模式開啟，則顯示回應
    }

    return response;
}

// 設置 UWB 配置的 AT 指令
String config_cmd() {
    String temp = "AT+SETCFG=";
    temp = temp + UWB_INDEX;     // 設定裝置 ID
    temp = temp + ",1";          // 設置裝置角色為 Anchor (1 = Anchor, 2 = Tag)
    temp = temp + ",1";          // 設置頻率為 6.8M (1 = 6.8M, 0 = 850k)
    temp = temp + ",1";          // 設置範圍過濾 (1 = 開啟, 0 = 關閉)
    return temp;
}

// 設置 UWB 容量的 AT 指令
String cap_cmd() {
    String temp = "AT+SETCAP=";
    temp = temp + UWB_TAG_COUNT; // 設定 UWB Tag 數量
    temp = temp + ",10";         // 設置單個時槽的時間
    return temp;
}
