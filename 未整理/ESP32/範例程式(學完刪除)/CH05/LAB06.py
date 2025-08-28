from machine import SoftI2C, Pin
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter, IIR_filter


my_SCL_pin = 25         # I2C SCL 腳位
my_SDA_pin = 26         # I2C SDA 腳位

i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin))

sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

pox = Pulse_oximeter(sensor)

dc_extractor = IIR_filter(0.99)  # 用於提取直流成份

while True:
    pox.update()                 # 更新血氧模組

    if pox.available():
        red_val = pox.get_raw_red()

        red_dc = dc_extractor.step(red_val)
        ppg = int(red_dc*1.01 - red_val)

        print(ppg)
