from machine import Pin
import utime

led = Pin(2, Pin.OUT)
while True:
    led.value(0) # 輸出0
    utime.sleep(1)
    led.value(1)
    utime.sleep(1) # 輸出1
