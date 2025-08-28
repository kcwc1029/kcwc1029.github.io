##################################################
# 經過rssi.py測試成功後
# 過來計算三角測量法獲得XY + 卡爾曼濾波器
# 
# 卡爾曼濾波器(Kalman Filter)：
# 對從 UWB 傳感器接收到的距離數據進行濾波，減少測量誤差和噪聲，從而提高位置計算的精度。
##################################################

import serial
import math
import time
import re
import paho.mqtt.client as mqtt

# MQTT 設置
broker_address = "140.116.179.56"  # 替換為您的 MQTT 伺服器地址
port = 1883
topic_x = "sensor/x"  # 用於發佈位置信息的主題
topic_y = "sensor/y"  # 用於發佈位置信息的主題

#### 手動輸入 COM 端口 (如 COM7) #####
com_port = "COM4"

class KalmanFilter:
    def __init__(self, process_variance, measurement_variance, estimate_variance):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimate_variance = estimate_variance
        self.current_estimate = 0
        self.last_estimate = 0
        self.kalman_gain = 0

    def update_estimate(self, measurement):
        self.kalman_gain = self.estimate_variance / (self.estimate_variance + self.measurement_variance)
        self.current_estimate = self.last_estimate + self.kalman_gain * (measurement - self.last_estimate)
        self.estimate_variance = (1 - self.kalman_gain) * self.estimate_variance + abs(self.last_estimate - self.current_estimate) * self.process_variance
        self.last_estimate = self.current_estimate
        return self.current_estimate

class UWB:
    def __init__(self, name, is_tag=False):
        self.name = name
        self.x = 0
        self.y = 0
        self.status = False
        self.ranges = []
        self.is_tag = is_tag
        self.kf_r1 = KalmanFilter(1e-5, 1e-2, 1e-3)
        self.kf_r2 = KalmanFilter(1e-5, 1e-2, 1e-3)
        self.kf_r3 = KalmanFilter(1e-5, 1e-2, 1e-3)

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.status = True

    def update_ranges(self, ranges):
        self.ranges = [
            self.kf_r1.update_estimate(ranges[0]),
            self.kf_r2.update_estimate(ranges[1]),
            self.kf_r3.update_estimate(ranges[2])
        ]

    def calculate_position(self, anchors):
        if len(self.ranges) >= 3:
            x, y = self.triangulate_position(anchors)
            self.set_location(x, y)
            print(f"{self.name} 的計算座標為: ({x}, {y})")
            return x, y  # 返回計算出的座標以發佈到 MQTT

    def triangulate_position(self, anchors):
        a1 = anchors[0]
        a2 = anchors[1]
        a3 = anchors[2]

        x1, y1, r1 = a1.x, a1.y, self.ranges[0]
        x2, y2, r2 = a2.x, a2.y, self.ranges[1]
        x3, y3, r3 = a3.x, a3.y, self.ranges[2]

        return self.triangulate(x1, y1, r1, x2, y2, r2, x3, y3, r3)

    def triangulate(self, x1, y1, r1, x2, y2, r2, x3, y3, r3):
        x_total = 0.0
        y_total = 0.0

        temp_x1, temp_y1 = self.interpolate(x1, y1, x2, y2, r1, r2)
        temp_x2, temp_y2 = self.interpolate(x1, y1, x3, y3, r1, r3)
        temp_x3, temp_y3 = self.interpolate(x2, y2, x3, y3, r2, r3)

        x_total = (temp_x1 + temp_x2 + temp_x3) / 3
        y_total = (temp_y1 + temp_y2 + temp_y3) / 3

        x_total = max(x_total, 0)
        y_total = max(y_total, 0)

        return x_total, y_total

    def interpolate(self, x1, y1, x2, y2, r1, r2):
        p2p = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        if p2p == 0:
            return x1, y1

        if r1 + r2 <= p2p:
            interp_x = x1 + (x2 - x1) * r1 / (r1 + r2)
            interp_y = y1 + (y2 - y1) * r1 / (r1 + r2)
        else:
            dr = (r1**2 - r2**2 + p2p**2) / (2 * p2p)
            interp_x = x1 + (x2 - x1) * dr / p2p
            interp_y = y1 + (y2 - y1) * dr / p2p

        return interp_x, interp_y

def parse_range_data(line):
    match = re.search(r'range:\((.*?)\)', line)
    if match:
        range_str = match.group(1)
        ranges = list(map(float, range_str.split(',')))
        return ranges
    return None

# MQTT 連接回調
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

def on_publish(client, userdata, mid):
    print("Data published with mid: " + str(mid))

def main():
    # MQTT 客戶端設置
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(broker_address, port, 60)
    
    # 設置三個 Anchor 的座標
    anchors = [
        UWB("Anchor 1"),
        UWB("Anchor 2"),
        UWB("Anchor 3")
    ]
    anchors[0].set_location(0, 0)
    anchors[1].set_location(0, 378)
    anchors[2].set_location(110, 378)

    # 創建一個 Tag
    tag = UWB("Tag 1", is_tag=True)

    # 打開串口
    ser = serial.Serial(com_port, 115200, timeout=1)
    time.sleep(2)

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                ranges = parse_range_data(line)
                if ranges and len(ranges) >= 3:
                    tag.update_ranges(ranges[:3])
                    x, y = tag.calculate_position(anchors)

                    ##### 處理x
                    if x<=0: x=0
                    elif x>0 and x<50: x=50
                    elif x>50 and x<100: x=100
                    elif x>100 and x<150: x=150
                    elif x>150 and x<200: x=200
                    elif x>200 and x<250: x=250
                    else: x=250

                    ##### 處理y
                    if y<=0: y=0
                    elif y>0 and y<48: y=48
                    elif y>48 and y<96: y=96
                    elif y>96 and y<144: y=144
                    elif y>144 and y<192: y=192
                    elif y>192 and y<240: y=240
                    elif y>240 and y<288: y=288
                    elif y>288 and y<336: y=336
                    elif y>336 and y<384: y=384
                    elif y>384 and y<432: y=432
                    elif y>432 and y<480: y=480
                    else: y=480

                    
                    if x is not None and y is not None:
                        # 發佈位置信息到 MQTT
                        msg_x = str(x)
                        msg_y = str(y)
                        result = client.publish(topic_x, msg_x)
                        result_x = client.publish(topic_x, msg_x)  # 發送 x 的消息
                        result_x.wait_for_publish()  # 確認 x 發佈成功

                        result_y = client.publish(topic_y, msg_y)  # 發送 y 的消息
                        result_y.wait_for_publish()  # 確認 y 發佈成功

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("停止程式")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
