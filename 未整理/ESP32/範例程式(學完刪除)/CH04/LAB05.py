# 匯入 utime 模組用以計時
from utime import ticks_ms, ticks_diff
from machine import SoftI2C, Pin
import network, ESPWebServer
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter


my_SCL_pin = 25         # I2C SCL 腳位
my_SDA_pin = 26         # I2C SDA 腳位

i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin))

sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

pox = Pulse_oximeter(sensor) # 使用血氧濃度計算類別

spo2 = 0

def SendSpo2(socket, args):  # 處理 /handleCmd 指令的函式
    ESPWebServer.ok(socket, "200", str(spo2))

print("連接中...")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("無線網路名稱", "無線網路密碼")

while not sta.isconnected():
    pass

print("已連接, ip為:", sta.ifconfig()[0])

ESPWebServer.begin(80)                     # 啟用網站
ESPWebServer.onPath("/measure", SendSpo2)  

time_mark = ticks_ms()
while True:
    ESPWebServer.handleClient()

    pox.update()

    spo2_tmp = pox.get_spo2()
    spo2_tmp = round(spo2_tmp, 1)

    if spo2_tmp > 0:
        time_mark = ticks_ms()
        spo2 = spo2_tmp
        print("SpO2:", spo2, "%")
        
    if ticks_diff(ticks_ms(), time_mark) > 5000:
        spo2 = 0
