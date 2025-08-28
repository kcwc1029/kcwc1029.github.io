from utime import ticks_ms, ticks_diff
from machine import Pin, ADC


adc_pin = Pin(36)          # 36是ESP32的VP腳位
adc = ADC(adc_pin)         # 設定36為輸入腳位
adc.width(ADC.WIDTH_10BIT) # 設定分辨率位元數(解析度)
adc.atten(ADC.ATTN_11DB)   # 設定最大電壓

max_val = 0                # 用來紀錄最大值
time_mark = ticks_ms()     # 取得當前時間

while True:
    raw_val = adc.read()
    if raw_val > max_val:
        max_val = raw_val

    if ticks_diff(ticks_ms(), time_mark) > 50:
        ecg = max_val
        print(ecg)

        max_val = 0
        time_mark = ticks_ms()    # 重置計時器
