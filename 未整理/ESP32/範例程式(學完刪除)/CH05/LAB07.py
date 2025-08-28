import _thread
from utime import ticks_ms, ticks_diff
from machine import SoftI2C, Pin
import network, ESPWebServer
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter, IIR_filter


led = Pin(5, Pin.OUT)
led.value(1)

my_SCL_pin = 25         # I2C SCL 腳位
my_SDA_pin = 26         # I2C SDA 腳位

i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin))

sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

pox = Pulse_oximeter(sensor)

dc_extractor = IIR_filter(0.99)    # 用於提取直流成分
thresh_generator = IIR_filter(0.9) # 用於產生動態閾值

is_beating = False             # 紀錄是否正在跳動的旗標
beat_time_mark = ticks_ms()    # 紀錄心跳時間點
heart_rate = 0
num_beats = 0         # 紀錄心跳次數
target_n_beats = 3    # 設定要幾次心跳才更新一次心率
tot_intval = 0        # 紀錄心跳時間區間
ppg = 0

def cal_heart_rate(intval, target_n_beats=3):
    intval /= 1000
    heart_rate = target_n_beats/(intval/60)
    heart_rate = round(heart_rate, 1)
    return heart_rate

def SendHrRate(socket, args):  # 處理 /hr 指令的函式
    ESPWebServer.ok(socket, "200", str(heart_rate))

def SendEcg(socket, args):     # 處理 /line 指令的函式
    ESPWebServer.ok(socket, "200", str(ppg))

def web_thread():    # 處理網頁的子執行緒函式
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

_thread.start_new_thread(web_thread, ())    # 啟動子執行緒

while True:         # 主執行緒
    pox.update()    # 更新血氧模組

    if pox.available():
        red_val = pox.get_raw_red()
        red_dc = dc_extractor.step(red_val)
        ppg = max(int(red_dc*1.01 - red_val), 0)
        thresh = thresh_generator.step(ppg)

        if ppg > (thresh + 20) and not is_beating:
            is_beating = True
            led.value(0)

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
        elif ppg < thresh:
            is_beating = False
            led.value(1)
