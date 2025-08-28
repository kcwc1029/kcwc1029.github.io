import time
from machine import Pin, ADC


adc_pin = Pin(36)          # 36是ESP32的VP腳位
adc = ADC(adc_pin)         # 設定36為輸入腳位
adc.width(ADC.WIDTH_10BIT) # 設定分辨率位元數(解析度)
adc.atten(ADC.ATTN_11DB)   # 設定最大電壓

data = 0                   # 資料總和
num_data = 1               # 資料筆數
f = open('temperature.txt', 'w')     # 開啟txt檔

print(adc.read())          # 先顯示一次, 確認數值是否正常

while True:
    print('第' + str(num_data) + '筆')# 顯示紀錄第幾筆
    temp = input("現在溫度:")         # 輸入實際溫度

    if temp == 'end':
        break

    for i in range(20):        # 重複20次
        thermal = adc.read()   # ADC值
        data = data + thermal  # 加總至data
        time.sleep(0.01)

    data = int(data/20)        # 取平均
    print('熱敏電阻:', data)
    print('')                  # 多空一行
    f.write(str(data) + ' ' + temp + '\n')  # data存到檔案中

    data = 0       # 總和歸0
    num_data += 1  # 次數加1
f.close()
