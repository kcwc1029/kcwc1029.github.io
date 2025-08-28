from utime import ticks_ms, ticks_diff
from machine import Pin, ADC
from pulse_oximeter import IIR_filter

class BreathingMonitor:
    def __init__(self, adc_pin=34, led_pin=5, threshold_alpha=0.9, target_n_breath=2):
        # 初始化硬體設置
        self.led = Pin(led_pin, Pin.OUT)
        self.led.value(1)

        self.adc_pin = Pin(adc_pin)
        self.adc = ADC(self.adc_pin)
        self.adc.width(ADC.WIDTH_10BIT)
        self.adc.atten(ADC.ATTN_11DB)

        self.thresh_generator = IIR_filter(threshold_alpha)

        # 初始化變數
        self.is_breathing = False
        self.breath_time_mark = ticks_ms()
        self.rsp_rate = 0
        self.num_breath = 0
        self.target_n_breath = target_n_breath
        self.tot_intval = 0
        self.rsp = 0

    def cal_rsp_rate(self, intval):
        """計算呼吸速率"""
        intval /= 1000
        rsp_rate = self.target_n_breath / (intval / 60)
        rsp_rate = round(rsp_rate, 1)
        return rsp_rate

    def monitor(self):
        """呼吸監控主迴圈"""
        time_mark = ticks_ms()
        while True:
            if ticks_diff(ticks_ms(), time_mark) > 300:
                self.rsp = self.adc.read()
                thresh = self.thresh_generator.step(self.rsp)

                if self.rsp > (thresh + 3) and not self.is_breathing:
                    self.is_breathing = True
                    self.led.value(0)

                    intval = ticks_diff(ticks_ms(), self.breath_time_mark)
                    if 60000 > intval > 1000:
                        self.tot_intval += intval
                        self.num_breath += 1
                        if self.num_breath == self.target_n_breath:
                            self.rsp_rate = self.cal_rsp_rate(self.tot_intval)
                            print(f"呼吸速率: {self.rsp_rate} bpm")
                            self.tot_intval = 0
                            self.num_breath = 0
                    else:
                        self.tot_intval = 0
                        self.num_breath = 0
                    self.breath_time_mark = ticks_ms()

                elif self.rsp < thresh:
                    self.is_breathing = False
                    self.led.value(1)

                time_mark = ticks_ms()  # 重置定時器

if __name__ == "__main__":
    monitor = BreathingMonitor()
    monitor.monitor()
