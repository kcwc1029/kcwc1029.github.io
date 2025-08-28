import _thread
import time
from machine import Pin, ADC
import network, ESPWebServer
from keras_lite import Model  # 從 keras_lite 模組匯入 Model
import ulab as np             # 匯入 ulab 模組並命名為 np


model = Model('temperature_model.json')     # 建立模型物件

# 增加神經網路的參數與模型
mean = 637.7357512953367  #平均值
std = 217.74074905622302  #標準差

adc_pin = Pin(36) 
adc = ADC(adc_pin)
adc.width(ADC.WIDTH_10BIT)
adc.atten(ADC.ATTN_11DB)

temp = 0                   # 溫度

def cal_temp(data):
    data = np.array([data])  # 將data轉換成array格式
    data = data - mean       # data減掉平均數
    data = data/std          # data除以標準差

    temp = model.predict(data)    # 得出預測值
    temp = round(temp[0]*100, 1)  # 將預測值×100等於預測溫度
    return temp

def SendTemp(socket, args):    # 處理 /measure 指令的函式
    ESPWebServer.ok(socket, "200", str(temp))
    
def web_thread():    # 處理網頁的子執行緒函式
    while True:
        ESPWebServer.handleClient()

print("連接中...")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("無線網路名稱", "無線網路密碼")

while not sta.isconnected():
    pass

print("已連接, ip為:", sta.ifconfig()[0])

ESPWebServer.begin(80)                   # 啟用網站
ESPWebServer.onPath("/measure", SendTemp)# 指定處理指令的函式

_thread.start_new_thread(web_thread, ()) # 啟動子執行緒

while True:
    data = 0
    for i in range(20):        # 重複20次
        thermal = adc.read()   # ADC值
        data = data + thermal  # 加總至data
        time.sleep(0.01)
    data = int(data/20)        # 取平均

    temp = cal_temp(data)
    print(temp)
    
