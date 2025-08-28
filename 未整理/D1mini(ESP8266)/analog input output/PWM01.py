# TODO: 建立PWM物件
from machine import Pin, PWM
import utime

pin = Pin(15, Pin.OUT)
led_pwm = PWM(pin,
			freq=1000 # 切換頻率
			duty=512 # 勤務循環(duty cycle)控致電壓(0-1023)
			)