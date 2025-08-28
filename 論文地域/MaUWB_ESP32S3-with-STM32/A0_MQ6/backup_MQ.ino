// #include <WiFi.h>
// #include <PubSubClient.h>

// // WiFi 配置
// const char* ssid = "ALHC_Lab";          // WiFi 網路名稱
// const char* password = "ALHC87878787";  // WiFi 密碼

// // MQTT 伺服器配置
// const char* mqtt_server = "140.116.179.56";  // MQTT 伺服器的 IP 或域名
// const int mqtt_port = 1883;                  // MQTT 伺服器端口
// const char* mqtt_user = "";                  // MQTT 使用者名稱
// const char* mqtt_password = "";              // MQTT 密碼

// WiFiClient espClient;
// PubSubClient client(espClient);

// #define MQ6_PIN 2  // MQ6 感測器接在 GPIO2
// #define MQ7_PIN 5  // MQ7 感測器接在 GPIO5
// #define MQ8_PIN 6  // MQ8 感測器接在 GPIO6

// // 連接到 WiFi 的函數
// void setup_wifi() {
//   delay(10);
//   Serial.println();
//   Serial.print("Connecting to ");
//   Serial.println(ssid);

//   WiFi.begin(ssid, password);  // 開始連接 WiFi

//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }

//   Serial.println("");
//   Serial.println("WiFi connected");
// }

// // 連接到 MQTT 伺服器
// void reconnect() {
//   while (!client.connected()) {
//     Serial.print("Attempting MQTT connection...");
//     if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {  // 嘗試連接 MQTT 伺服器
//       Serial.println("connected");
//       client.subscribe("testTopic");  // 訂閱主題
//     } else {
//       Serial.print("failed, rc=");
//       Serial.print(client.state());
//       Serial.println(" try again in 5 seconds");
//       delay(5000);  // 連接失敗後等待 5 秒重試
//     }
//   }
// }

// void setup() {
//   Serial.begin(115200);
//   setup_wifi();                              // 連接 WiFi
//   client.setServer(mqtt_server, mqtt_port);  // 設置 MQTT 伺服器
// }

// void loop() {
//   if (!client.connected()) {
//     reconnect();  // 若未連接，嘗試重新連接
//   }
//   client.loop();  // MQTT 客戶端保持活躍

//   ///// 處理MQ6 /////
//   int MQ6_sensorValue = analogRead(MQ6_PIN);                        // 讀取 MQ6 感測器的數值
//   String MQ6_msg = "MQ6 Sensor Value: " + String(MQ6_sensorValue);  // 使用 String 類型進行格式化
//   Serial.print("Publishing message: ");
//   Serial.println(MQ6_msg);

//   ///// 處理MQ7 /////
//   int MQ7_sensorValue = analogRead(MQ7_PIN);                        // 讀取 MQ6 感測器的數值
//   String MQ7_msg = "MQ7 Sensor Value: " + String(MQ7_sensorValue);  // 使用 String 類型進行格式化
//   Serial.print("Publishing message: ");
//   Serial.println(MQ7_msg);

//   ///// 處理MQ8 /////
//   int MQ8_sensorValue = analogRead(MQ8_PIN);                        // 讀取 MQ6 感測器的數值
//   String MQ8_msg = "MQ8 Sensor Value: " + String(MQ8_sensorValue);  // 使用 String 類型進行格式化
//   Serial.print("Publishing message: ");
//   Serial.println(MQ8_msg);

//   // 將 String 類型轉為 C 字串發佈到 MQTT 主題
//   client.publish("sensor/mq6", MQ6_msg.c_str());  // 使用 .c_str() 將 String 轉換為 C 字串
//   client.publish("sensor/mq7", MQ7_msg.c_str());  // 使用 .c_str() 將 String 轉換為 C 字串
//   client.publish("sensor/mq8", MQ8_msg.c_str());  // 使用 .c_str() 將 String 轉換為 C 字串
//   delay(1000);                                    // 每秒發送一次數據
// }
