import utime
from machine import Pin

led = Pin(2, Pin.OUT)
led.value(1)
while True:
    v = led.value() # 讀取狀態
    print("狀態值", v)
    v = not v
    print("更改狀態", v)
    led.value(v)
    utime.sleep(1)