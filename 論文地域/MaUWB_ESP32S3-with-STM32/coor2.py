##################################################
# 經過rssi.py測試成功後
# 過來計算三角測量法獲得XY
##################################################

import serial
import math
import time
import re

#### 手動輸入 COM 端口 (如 COM7) #####
com_port = "COM4"

class UWB:
    def __init__(self, name, is_tag=False):
        self.name = name
        self.x = 0
        self.y = 0
        self.status = False
        self.ranges = []  # 用於存儲到各 Anchor 的距離
        self.is_tag = is_tag  # 判斷是 Anchor 還是 Tag

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.status = True

    def update_ranges(self, ranges):
        self.ranges = ranges

    def calculate_position(self, anchors):
        # 確保有足夠的 Anchor 進行計算
        if len(self.ranges) >= 3:
            x, y = self.triangulate_position(anchors)
            self.set_location(x, y)
            print(f"{self.name} 的計算座標為: ({x}, {y})")

    def triangulate_position(self, anchors):
        # 使用兩個 Anchor 來計算位置（距離插值方法）
        a1 = anchors[0]
        a2 = anchors[1]
        a3 = anchors[2]

        # 取得三個 Anchor 之間的距離
        x1, y1, r1 = a1.x, a1.y, self.ranges[0]
        x2, y2, r2 = a2.x, a2.y, self.ranges[1]
        x3, y3, r3 = a3.x, a3.y, self.ranges[2]

        # 使用距離插值方法來計算座標
        return self.triangulate(x1, y1, r1, x2, y2, r2, x3, y3, r3)

    def triangulate(self, x1, y1, r1, x2, y2, r2, x3, y3, r3):
        # 利用兩點之間的距離和插值方法計算位置
        x_total = 0.0
        y_total = 0.0

        # 使用插值方法計算兩個 Anchor 的相對位置
        temp_x1, temp_y1 = self.interpolate(x1, y1, x2, y2, r1, r2)
        temp_x2, temp_y2 = self.interpolate(x1, y1, x3, y3, r1, r3)
        temp_x3, temp_y3 = self.interpolate(x2, y2, x3, y3, r2, r3)

        # 將三個插值結果取平均值作為最終位置
        x_total = (temp_x1 + temp_x2 + temp_x3) / 3
        y_total = (temp_y1 + temp_y2 + temp_y3) / 3

        # 防止出現負數座標
        x_total = max(x_total, 0)
        y_total = max(y_total, 0)

        return x_total, y_total

    def interpolate(self, x1, y1, x2, y2, r1, r2):
        # 計算圓心距
        p2p = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # 判斷是否相交並進行線性插值計算
        if r1 + r2 <= p2p:
            # 當距離過大時，直接插值兩者的中點
            interp_x = x1 + (x2 - x1) * r1 / (r1 + r2)
            interp_y = y1 + (y2 - y1) * r1 / (r1 + r2)
        else:
            # 使用加權平均計算位置
            dr = p2p / 2 + (r1 ** 2 - r2 ** 2) / (2 * p2p)
            interp_x = x1 + (x2 - x1) * dr / p2p
            interp_y = y1 + (y2 - y1) * dr / p2p

        return interp_x, interp_y

def parse_range_data(line):
    # 使用正則表達式提取 range 內的數據
    match = re.search(r'range:\((.*?)\)', line)
    if match:
        range_str = match.group(1)  # 提取 range 內的數字部分
        ranges = list(map(float, range_str.split(',')))  # 將字符串轉換為浮點數列表
        return ranges
    return None

def main():
    # 設置三個 Anchor 的座標
    anchors = [
        UWB("Anchor 1"),
        UWB("Anchor 2"),
        UWB("Anchor 3")
    ]
    # 使用你提供的新的座標
    anchors[0].set_location(0, 0)         # Anchor 1 的座標
    anchors[1].set_location(0, 378)      # Anchor 2 的座標
    anchors[2].set_location(175, 378)      # Anchor 3 的座標

    # 創建一個 Tag
    tag = UWB("Tag 1", is_tag=True)

    # 打開串口，假設串口設備是 COM7 並且波特率是 115200
    ser = serial.Serial(com_port, 115200, timeout=1)
    time.sleep(2)  # 給串口一些時間來穩定

    try:
        while True:
            # 假設從串口接收到的數據是距離數據
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                # 解析數據
                ranges = parse_range_data(line)
                if ranges and len(ranges) >= 3:
                    # 只取前三個有效距離數據
                    tag.update_ranges(ranges[:3])

                    # 計算 Tag 的位置
                    tag.calculate_position(anchors)
                else:
                    print("無法解析數據:", line)

            time.sleep(1)  # 可以設置適當的延遲來降低CPU負擔

    except KeyboardInterrupt:
        print("停止程式")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
