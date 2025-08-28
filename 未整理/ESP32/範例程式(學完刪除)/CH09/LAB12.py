from machine import Pin, ADC


f = open('test.txt', 'w')

adc_pin = Pin(36)
adc = ADC(adc_pin)
adc.width(ADC.WIDTH_10BIT)
adc.atten(ADC.ATTN_11DB)
temp = input('請輸入現在溫度:')

f.write(str(adc.read()) + ' ' + temp)    # 以空格隔開ADC值與溫度值
f.close()
