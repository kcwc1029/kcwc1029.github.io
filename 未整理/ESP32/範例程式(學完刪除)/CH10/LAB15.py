from utime import ticks_ms, ticks_diff
from machine import Pin, ADC, SoftI2C
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter, IIR_filter


led = Pin(5, Pin.OUT)
led.value(1)

adc_pin = Pin(36)          # 36是ESP32的VP腳位
adc = ADC(adc_pin)         # 設定36為輸入腳位 
adc.width(ADC.WIDTH_10BIT) # 設定分辨率位元數(解析度)
adc.atten(ADC.ATTN_11DB)   # 設定最大電壓

my_SCL_pin = 25         # I2C SCL 腳位
my_SDA_pin = 26         # I2C SDA 腳位

i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin))

sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

pox = Pulse_oximeter(sensor)

thresh_gen_pulse = IIR_filter(0.9) # 用於產生PPG的動態閾值
thresh_gen_heart = IIR_filter(0.9) # 用於產生ECG的動態閾值
dc_extractor = IIR_filter(0.99)    # 用於提取DC成分

detected_heart_beat = False
pulse_is_beating = False
heart_is_beating = False
pulse_time_mark = ticks_ms()
heart_time_mark = ticks_ms()
max_ecg = 0

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
        ppg = int(red_dc*1.01 - red_val)
        thresh_pulse = thresh_gen_pulse.step(ppg)

        ##---------------偵測心跳開始---------------#
        if ecg > (thresh_heart + 100) and not \
        heart_is_beating:
            print("heart beat!")
            detected_heart_beat = True
            heart_is_beating = True
            heart_time_mark = ticks_ms()
        elif ecg < thresh_heart:
            heart_is_beating = False
        ##---------------偵測心跳結束---------------#

        ##---------------偵測脈搏開始---------------#
        if ppg > (thresh_pulse + 20) and not \
        pulse_is_beating:
            led.value(0)
            print("pulse beat!")
            pulse_is_beating = True
            pulse_time_mark = ticks_ms()

            if detected_heart_beat:
                pwtt = ticks_diff(pulse_time_mark,
                                  heart_time_mark)
                print("pwtt =", pwtt)
                detected_heart_beat = False

        elif ppg < thresh_pulse:
            led.value(1)
            pulse_is_beating = False
        #---------------偵測脈搏結束---------------#
        max_ecg = 0
