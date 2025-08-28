from utime import ticks_ms, ticks_diff
from machine import Pin, ADC


adc_pin = Pin(32)
adc = ADC(adc_pin)
adc.width(ADC.WIDTH_10BIT)
adc.atten(ADC.ATTN_11DB)

time_mark = ticks_ms()
while True:
    if ticks_diff(ticks_ms(), time_mark) > 300:
        rsp = adc.read()
        print(f"rsp: {rsp}")
        time_mark = ticks_ms()    # 重置定時器

