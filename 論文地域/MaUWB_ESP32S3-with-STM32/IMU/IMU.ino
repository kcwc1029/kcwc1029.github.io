// 定義引腳
const int xPin = 5;  // X 軸接 ESP32 的 GPIO34
const int yPin = 6;  // Y 軸接 ESP32 的 GPIO35
const int zPin = 7;  // Z 軸接 ESP32 的 GPIO32

// 定義靈敏度
const float sensitivity = 800.0;  // 每 G 的電壓靈敏度 (根據您的感測器設置)
const float zeroG_voltage = 1.65; // 感測器的 0G 基準電壓 (通常是 VCC/2)

void setup() {
  // put your setup code here, to run once:
  // 初始化序列監控
  Serial.begin(115200);
  delay(1000); // 等待系統穩定
}

void loop() {
  // 讀取類比值 (範圍 0 - 4095)
  int xRaw = analogRead(xPin);
  int yRaw = analogRead(yPin);
  int zRaw = analogRead(zPin);

  // 將類比值轉換為電壓 (ESP32 的 ADC 是 12 位精度，範圍是 0 到 3.3V)
  float xVoltage = xRaw * (3.3 / 4095.0);
  float yVoltage = yRaw * (3.3 / 4095.0);
  float zVoltage = zRaw * (3.3 / 4095.0);

  // 將電壓轉換為加速度 (單位 G)
  float xG = (xVoltage - zeroG_voltage) / (sensitivity / 1000.0);
  float yG = (yVoltage - zeroG_voltage) / (sensitivity / 1000.0);
  float zG = (zVoltage - zeroG_voltage) / (sensitivity / 1000.0);

  // 在序列監控器中顯示結果
  Serial.print("X軸加速度: ");
  Serial.print(xG);
  Serial.print("G, Y軸加速度: ");
  Serial.print(yG);
  Serial.print("G, Z軸加速度: ");
  Serial.print(zG);
  Serial.println("G");

  // 延遲 500 毫秒
  delay(500);
}
