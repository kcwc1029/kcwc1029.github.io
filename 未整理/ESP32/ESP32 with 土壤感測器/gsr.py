import time
from machine import Pin, ADC

def init_gsr():
    ADC_PIN = Pin(36)
    adc = ADC(ADC_PIN)
    adc.width(ADC.WIDTH_9BIT)
    adc.atten(ADC.ATTN_11DB)
    return adc

def read_gsr(adc):
    """從指定的 ADC 實例中讀取 GSR 數據"""
    return adc.read()

# GSR 任務函數
def gsr_task():
    adc = init_gsr()
    read_gsr(adc)
    while True:
        gsr_value = read_gsr(adc)
        print(f"GSR: {gsr_value}")
        time.sleep(1)

if __name__ == "__main__":
    gsr_task()