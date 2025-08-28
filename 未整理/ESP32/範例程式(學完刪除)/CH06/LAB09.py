import _thread
from utime import ticks_ms, ticks_diff
from machine import Pin, ADC
import network, ESPWebServer
from pulse_oximeter import IIR_filter


buzzer = Pin(2, Pin.OUT)

adc_pin = Pin(36)           # 36是ESP32的VP腳位
adc = ADC(adc_pin)          # 設定36為輸入腳位
adc.width(ADC.WIDTH_10BIT)  # 設定分辨率位元數(解析度)
adc.atten(ADC.ATTN_11DB)    # 設定最大電壓

thresh_generator = IIR_filter(0.9) # 用於產生動態閾值

is_beating = False             # 紀錄是否正在跳動的旗標
beat_time_mark = ticks_ms()    # 紀錄心跳時間點
heart_rate = 0
num_beats = 0                  # 紀錄心跳次數
target_n_beats = 3             # 設定要幾次心跳才更新一次心率
tot_intval = 0                 # 紀錄心跳時間區間
max_val = 0
ecg = 0

def cal_heart_rate(intval, target_n_beats=3):
    intval /= 1000
    heart_rate = target_n_beats/(intval/60)
    heart_rate = round(heart_rate, 1)
    return heart_rate

def SendHrRate(socket, args):    # 處理 /hr 指令的函式
    ESPWebServer.ok(socket, "200", str(heart_rate))

def SendEcg(socket, args):       # 處理 /line 指令的函式
    ESPWebServer.ok(socket, "200", str(ecg))

def web_thread():
    while True:
        ESPWebServer.handleClient()

print("連接中...")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("無線網路名稱", "無線網路密碼")

while not sta.isconnected():
    pass

print("已連接, ip為:", sta.ifconfig()[0])

ESPWebServer.begin(80)                  # 啟用網站
ESPWebServer.onPath("/hr", SendHrRate)  # 指定處理指令的函式
ESPWebServer.onPath("/line", SendEcg)   # 指定處理指令的函式

_thread.start_new_thread(web_thread, ())

time_mark = ticks_ms()

while True:
    raw_val = adc.read()

    if raw_val > max_val:
        max_val = raw_val

    if ticks_diff(ticks_ms(), time_mark) > 50:
        ecg = max_val
        thresh = thresh_generator.step(ecg)

        if ecg > (thresh + 100) and not is_beating:
            is_beating = True
            buzzer.value(1)

            intval = ticks_diff(ticks_ms(), beat_time_mark)
            if 2000 > intval > 270:
                tot_intval += intval
                num_beats += 1
                if num_beats == target_n_beats:
                    heart_rate = cal_heart_rate(
                        tot_intval, target_n_beats)
                    print(heart_rate)
                    tot_intval = 0
                    num_beats = 0
            else:
                tot_intval = 0
                num_beats = 0
            beat_time_mark = ticks_ms()

        elif ecg < thresh:
            is_beating = False
            buzzer.value(0)

        max_val = 0
        time_mark = ticks_ms()
