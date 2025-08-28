import time
from machine import Pin, ADC


adc_pin = Pin(36)         # 36是ESP32的VP腳位
adc = ADC(adc_pin)        # 設定36為輸入腳位
adc.width(ADC.WIDTH_9BIT) # 設定分辨率位元數(解析度)
adc.atten(ADC.ATTN_11DB)  # 設定最大電壓

while True:
    gsr = adc.read()
    print(gsr)
    time.sleep(0.1)
    