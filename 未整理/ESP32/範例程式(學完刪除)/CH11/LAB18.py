from utime import ticks_ms, ticks_diff
from machine import SoftI2C, Pin
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter, IIR_filter
from keras_lite import Model
import ulab as np


mean = 130.50358333333332 # 請改成訓練模型時的資料集平均數
std = 1514.8632605465837  # 請改成訓練模型時的資料集標準差
model = Model('ppg_model.json') # 建立模型物件
label_name = ['others', 'ppg']   # label名稱要與建立模型時的順序一樣


led = Pin(5, Pin.OUT)
led.value(1)

my_SCL_pin = 25         # I2C SCL 腳位
my_SDA_pin = 26         # I2C SDA 腳位

i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin))

sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

pox = Pulse_oximeter(sensor)

thresh_generator = IIR_filter(0.9) # 用於產生動態閾值
dc_extractor = IIR_filter(0.99)    # 用於提取直流成分

is_beating = False
beat_time_mark = ticks_ms()
heart_rate = 0
num_beats = 0
target_n_beats = 3
tot_intval = 0


def cal_heart_rate(intval, target_n_beats=3):
    intval /= 1000
    heart_rate = target_n_beats/(intval/60)
    heart_rate = round(heart_rate, 1)
    return heart_rate

def trim(data, length=300):
    if len(data) > length:
        data = data[:length]
    else:
        data = data + [0 for _ in range(length - len(data))]
    return data

def get_label(data):
    data = trim(data)
    data = np.array([data])
    data = (data - mean)/std
    pred_class = model.predict_classes(data)
    label = label_name[pred_class[0]]
    return label

data = []

while True:
    pox.update()

    if pox.available():
        red_val = pox.get_raw_red()
        red_dc = dc_extractor.step(red_val)
        ppg = int(red_dc*1.01 - red_val)
        data.append(ppg)
        thresh = thresh_generator.step(ppg)

        if ppg > (thresh + 20) and not is_beating:
            is_beating = True
            led.value(0)

            rr_intval = ticks_diff(
                ticks_ms(), beat_time_mark)
            if 2000 > rr_intval > 270:
                tot_intval += rr_intval
                num_beats += 1
                if num_beats == target_n_beats:
                    label = get_label(data)
                    print('類別:', label)
                    if label == "ppg":
                        heart_rate = cal_heart_rate(
                            tot_intval, target_n_beats)
                        print("心率:", heart_rate)
                    tot_intval = 0
                    num_beats = 0
                    data = []
            else:
                tot_intval = 0
                num_beats = 0
                data = []
            beat_time_mark = ticks_ms()
        elif ppg < thresh:
            is_beating = False
            led.value(1)
