import _thread
from utime import ticks_ms, ticks_diff
from machine import Pin, ADC, SoftI2C
import network, ESPWebServer
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter, IIR_filter
from keras_lite import Model  # 從 keras_lite 模組匯入 Model
import ulab as np             # 匯入 ulab 模組並命名為 np


model = Model('bp_model.json')     # 建立模型物件

led = Pin(5, Pin.OUT)
led.value(1)

adc_pin = Pin(36)          # 36是ESP32的VP腳位
adc = ADC(adc_pin)         # 設定36為輸入腳位          
adc.width(ADC.WIDTH_10BIT) # 設定分辨率位元數(解析度)
adc.atten(ADC.ATTN_11DB)   # 設定最大電壓

my_SCL_pin = 25            # I2C SCL 腳位
my_SDA_pin = 26            # I2C SDA 腳位

i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin))

sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

pox = Pulse_oximeter(sensor)

thresh_gen_pulse = IIR_filter(0.9) # 用於產生PPG的動態閾值
thresh_gen_heart = IIR_filter(0.9) # 用於產生ECG的動態閾值
dc_extractor = IIR_filter(0.99)    # 用於提取直流成分

detected_heart_beat = False
pulse_is_beating = False
heart_is_beating = False
pulse_time_mark = ticks_ms()
heart_time_mark = ticks_ms()
max_ecg = 0
heart_rate = 0
num_beats = 0
target_n_beats = 3
tot_intval = 0
bp = 0

def cal_heart_rate(intval, target_n_beats=3):
    intval /= 1000
    heart_rate = target_n_beats/(intval/60)
    heart_rate = round(heart_rate, 1)
    return heart_rate

def cal_bp(pwtt):
    pwtt /= 200
    pwtt = np.array([pwtt])
    bloop_pressure = model.predict(pwtt) # 得出預測值
    bloop_pressure = round(
        bloop_pressure[0]*100, 1) # 將預測值×100
    return bloop_pressure

def SendHrRate(socket, args):     # 處理 /hr 指令的函式
    ESPWebServer.ok(socket, "200", str(heart_rate))

def SendBP(socket, args):         # 處理 /line 指令的函式
    ESPWebServer.ok(socket, "200", str(bp))

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

ESPWebServer.begin(80)                  
ESPWebServer.onPath("/hr", SendHrRate)  
ESPWebServer.onPath("/bp", SendBP)      

_thread.start_new_thread(web_thread, ()) # 啟動子執行緒

while True:
    ecg_raw = adc.read()
    if ecg_raw > max_ecg:
        max_ecg = ecg_raw

    pox.update()

    if pox.available():
        ecg = max_ecg
        thresh_heart = thresh_gen_heart.step(ecg)

        red_val = pox.get_raw_red()
        red_dc = dc_extractor.step(red_val)
        ppg = red_dc*1.01 - red_val
        thresh_pulse = thresh_gen_pulse.step(ppg)

        #---------------偵測心跳開始---------------#
        if ecg > (thresh_heart + 100) and not\
        heart_is_beating:
            print("heart beat!")
            detected_heart_beat = True
            heart_is_beating = True
            heart_time_mark = ticks_ms()
        elif ecg < thresh_heart:
            heart_is_beating = False
        #---------------偵測心跳結束---------------#

        #---------------偵測脈搏開始---------------#
        if ppg > (thresh_pulse + 20) and not\
        pulse_is_beating:
            pulse_is_beating = True
            led.value(0)
            print("pulse beat!")

            rr_intval = ticks_diff(ticks_ms(),
                                   pulse_time_mark)

            if 2000 > rr_intval > 270:
                tot_intval += rr_intval
                num_beats += 1
                if num_beats == target_n_beats:
                    heart_rate = cal_heart_rate(
                        tot_intval, target_n_beats)
                    print("heart rate =", heart_rate)
                    tot_intval = 0
                    num_beats = 0
            else:
                tot_intval = 0
                num_beats = 0
            pulse_time_mark = ticks_ms()

            if detected_heart_beat:
                pwtt = ticks_diff(pulse_time_mark,
                                  heart_time_mark)
                print("pwtt =", pwtt)
                bp = cal_bp(pwtt)
                print("bp =", bp)
                detected_heart_beat = False

        elif ppg < thresh_pulse:
            pulse_is_beating = False
            led.value(1)
        #---------------偵測脈搏結束---------------#
        max_ecg = 0
