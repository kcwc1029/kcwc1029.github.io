# 匯入 utime 模組用以計時
from utime import ticks_ms, ticks_diff
from machine import Pin, ADC
import network, ESPWebServer


adc_pin = Pin(36)         # 36是ESP32的VP腳位
adc = ADC(adc_pin)        # 設定36為輸入腳位
adc.width(ADC.WIDTH_9BIT) # 設定分辨率位元數(解析度)
adc.atten(ADC.ATTN_11DB)  # 設定最大電壓

angle = 180               # 膚電反應轉換後角度

def SendAngle(socket, args):    # 處理 /lie 指令的函式
    ESPWebServer.ok(socket, "200", str(angle))

# 將膚電反應對應到180~360的函式
def gsr_to_angle(raw_val, min_val, max_val):  
    raw_val *= -1
    new_val = ((raw_val + max_val)
        /(max_val - min_val)*(360 - 180) + 180)
    return new_val

print("連接中...")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("無線網路名稱", "無線網路密碼")

while not sta.isconnected():
    pass

print("已連接, ip為:", sta.ifconfig()[0])

ESPWebServer.begin(80)                  # 啟用網站
ESPWebServer.onPath("/lie", SendAngle)  # 指定處理指令的函式

time_mark = ticks_ms()    # 取得當前時間
while True:
    # 持續檢查是否收到新指令
    ESPWebServer.handleClient()

    # 當計時器變數與現在的時間差小於 100 則執行任務
    if ticks_diff(ticks_ms(), time_mark) > 100:
        gsr = adc.read()
        angle = gsr_to_angle(gsr, 400, 511)
        time_mark = ticks_ms() # 重置計時器
