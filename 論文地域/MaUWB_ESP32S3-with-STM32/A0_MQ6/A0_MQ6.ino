#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// WiFi 配置
const char* ssid = "ALHC_Lab";          // WiFi 網路名稱
const char* password = "ALHC87878787";  // WiFi 密碼

// MQTT 伺服器配置
const char* mqtt_server = "140.116.179.56";  // MQTT 伺服器的 IP 或域名
const int mqtt_port = 1883;                  // MQTT 伺服器端口
const char* mqtt_user = "";                  // MQTT 使用者名稱
const char* mqtt_password = "";              // MQTT 密碼

WiFiClient espClient;
PubSubClient client(espClient);

// 感測器腳位配置
#define MQ6_PIN 2  // MQ6 感測器接在 GPIO2
#define MQ7_PIN 5  // MQ7 感測器接在 GPIO5
#define MQ8_PIN 6  // MQ8 感測器接在 GPIO6

// UWB 配置
#define UWB_INDEX 0  // 定義 UWB 裝置編號
#define ANCHOR      // 定義此裝置為「錨點」(Anchor)角色
#define FREQ_6800K  // 使用 6.8M 頻率
#define UWB_TAG_COUNT 64  // UWB 支持的 Tag 數量

// ESP32S3 I/O 定義
#define RESET 16   // RESET 腳位
#define IO_RXD2 18 // UART2 的 RXD
#define IO_TXD2 17 // UART2 的 TXD
#define I2C_SDA 39 // I2C 的 SDA 腳位
#define I2C_SCL 38 // I2C 的 SCL 腳位

HardwareSerial SERIAL_AT(2);    // 初始化第二組硬體序列端口，對應到 UART2
Adafruit_SSD1306 display(128, 64, &Wire, -1);  // 初始化 SSD1306 顯示器

// 連接到 WiFi 的函數
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);  // 開始連接 WiFi

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
}

// 連接到 MQTT 伺服器的函數
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {  // 嘗試連接 MQTT 伺服器
      Serial.println("connected");
      client.subscribe("testTopic");  // 訂閱主題
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);  // 連接失敗後等待 5 秒重試
    }
  }
}

// 顯示 Logo 及初始化信息
void logoshow(void) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println(F("MaUWB DW3000"));

  display.setCursor(0, 20);
  display.setTextSize(2);
  String temp = "A" + String(UWB_INDEX) + "   6.8M";
  display.println(temp);

  display.setCursor(0, 40);
  temp = "Total: " + String(UWB_TAG_COUNT);
  display.println(temp);
  display.display();
  delay(2000);
}

// 發送 AT 指令的通用函數
String sendData(String command, const int timeout, boolean debug) {
  String response = "";
  Serial.println(command);
  SERIAL_AT.println(command);

  long int time = millis();
  while ((time + timeout) > millis()) {
    while (SERIAL_AT.available()) {
      char c = SERIAL_AT.read();
      response += c;
    }
  }

  if (debug) {
    Serial.println(response);
  }

  return response;
}

// 設置 UWB 配置的 AT 指令
String config_cmd() {
  String temp = "AT+SETCFG=" + String(UWB_INDEX) + ",1,1,1";
  return temp;
}

// 設置 UWB 容量的 AT 指令
String cap_cmd() {
  String temp = "AT+SETCAP=" + String(UWB_TAG_COUNT) + ",10";
  return temp;
}

void setup() {
  // WiFi 和 MQTT 配置
  Serial.begin(115200);
  setup_wifi();                              // 連接 WiFi
  client.setServer(mqtt_server, mqtt_port);  // 設置 MQTT 伺服器

  // 初始化 UWB 和顯示器
  pinMode(RESET, OUTPUT);
  digitalWrite(RESET, HIGH);

  SERIAL_AT.begin(115200, SERIAL_8N1, IO_RXD2, IO_TXD2);
  Wire.begin(I2C_SDA, I2C_SCL);
  delay(1000);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.clearDisplay();
  logoshow();  // 顯示 Logo 和初始化信息

  sendData("AT?", 2000, 1);
  sendData("AT+RESTORE", 5000, 1);
  sendData(config_cmd(), 2000, 1);
  sendData(cap_cmd(), 2000, 1);
  sendData("AT+SETRPT=1", 2000, 1);
  sendData("AT+SAVE", 2000, 1);
  sendData("AT+RESTART", 2000, 1);
}

void loop() {
  // 處理 MQTT 連接
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // 處理感測器數據並上傳到 MQTT
  int MQ6_sensorValue = analogRead(MQ6_PIN);
  int MQ7_sensorValue = analogRead(MQ7_PIN);
  int MQ8_sensorValue = analogRead(MQ8_PIN);

  String MQ6_msg = String(MQ6_sensorValue);
  String MQ7_msg = String(MQ7_sensorValue);
  String MQ8_msg = String(MQ8_sensorValue);

  Serial.println(MQ6_msg);
  Serial.println(MQ7_msg);
  Serial.println(MQ8_msg);

  client.publish("sensor/mq6", MQ6_msg.c_str());
  client.publish("sensor/mq7", MQ7_msg.c_str());
  client.publish("sensor/mq8", MQ8_msg.c_str());

  delay(1000);  // 每秒發送一次數據

  // 處理 UWB 通訊
  if (SERIAL_AT.available() > 0) {
    String response = sendData("AT+RANGE", 2000, 1);
    Serial.println(response);
  }
}
