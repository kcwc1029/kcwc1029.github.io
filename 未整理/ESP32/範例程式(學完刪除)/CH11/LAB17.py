from utime import ticks_ms, ticks_diff
from machine import SoftI2C, Pin
from max30102 import MAX30102
from pulse_oximeter import Pulse_oximeter, IIR_filter


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
target_n_beats = 3    # 設定要幾次心跳才更新一次心率
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

data = []
file  = open('ppg.txt','w')    # 開啟txt檔
num_completed = 0
target_num = 50

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
                    heart_rate = cal_heart_rate(
                        tot_intval, target_n_beats)
                    data = trim(data)
                    for point in data:
                        print(point)
                    print("心率:", heart_rate)
                    yn = input("是否儲存(Y/N)?")
                    if yn in ("y", "Y", "yes"):
                        num_completed += 1
                        print("已儲存: %s/%s 筆資料" %
                              (num_completed, target_num))
                        # data存到檔案中
                        file.write(str(data)[1: -1])
                        # 換行字元
                        file.write("\n")             
                        if num_completed == target_num:
                            print("完成!")
                            break
                    else:
                        print("放棄儲存")
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

file.close()
