"""
利用PPG值去計算心率
"""
from utime import ticks_ms, ticks_diff
from machine import SoftI2C, Pin
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter, IIR_filter

def init_pulse_sensor(scl_pin=22, sda_pin=21):
    """初始化 MAX30102 傳感器"""
    i2c = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin))
    sensor = MAX30102(i2c=i2c)
    sensor.setup_sensor()
    return Pulse_oximeter(sensor)

def init_led(pin=5):
    """初始化 LED"""
    led = Pin(pin, Pin.OUT)
    led.value(1)
    return led

def cal_heart_rate(intval, target_n_beats=3):
    """計算心率"""
    intval /= 1000
    heart_rate = target_n_beats / (intval / 60)
    heart_rate = round(heart_rate, 1)
    return heart_rate

def monitor_heart_rate(pox, led, target_n_beats=3):
    """監控心率"""
    dc_extractor = IIR_filter(0.99)    # 用於提取直流成分
    thresh_generator = IIR_filter(0.9) # 用於產生動態閾值

    is_beating = False             # 紀錄是否正在跳動的旗標
    beat_time_mark = ticks_ms()    # 紀錄心跳時間點
    heart_rate = 0
    num_beats = 0         # 紀錄心跳次數
    tot_intval = 0        # 紀錄心跳時間區間

    while True:
        pox.update()    # 更新血氧模組

        if pox.available():
            red_val = pox.get_raw_red()
            red_dc = dc_extractor.step(red_val)
            ppg = max(int(red_dc * 1.01 - red_val), 0)
            thresh = thresh_generator.step(ppg)

            if ppg > (thresh + 20) and not is_beating:
                is_beating = True
                led.value(0)

                intval = ticks_diff(ticks_ms(), beat_time_mark)
                if 2000 > intval > 270:
                    tot_intval += intval
                    num_beats += 1
                    if num_beats == target_n_beats:
                        heart_rate = cal_heart_rate(tot_intval, target_n_beats)
                        print("Heart Rate:", heart_rate, "BPM")
                        tot_intval = 0
                        num_beats = 0
                else:
                    tot_intval = 0
                    num_beats = 0
                beat_time_mark = ticks_ms()
            elif ppg < thresh:
                is_beating = False
                led.value(1)

def ppg_pluse_task():
    pox = init_pulse_sensor()
    led = init_led()
    monitor_heart_rate(pox, led)

if __name__ == "__main__":
    ppg_pluse_task()

