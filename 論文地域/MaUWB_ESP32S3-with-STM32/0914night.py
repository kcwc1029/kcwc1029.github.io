# 因為次是還是覺得怪怪的，就重新寫
import serial
import serial.tools.list_ports  # 確保匯入 list_ports
import json
import time
import math

#### 手動輸入 COM 端口 (如 COM7) #####
com_port = "COM7"

def list_available_com_ports():
    """列出所有可用的 COM 端口"""
    ports = list(serial.tools.list_ports.comports())
    if len(ports) == 0:
        print("沒有發現可用的 COM 端口")
        return None
    print("可用的 COM 端口如下:")
    for port in ports:
        print(f"{port.device} - {port.description}")
    return ports

def read_esp32_data(ser, anchors):
    """從 ESP32 讀取數據並解析 AT 指令中的範圍 (range) 和 RSSI"""
    while True:
        line = ser.readline().decode('utf-8').strip()  # 讀取一行並進行解碼和去除空白
        print(f"讀取到的數據: {line}")
        
        # 嘗試解析 AT 指令格式的數據
        if "AT+RANGE" in line:
            try:
                # 提取範圍數據和 RSSI
                start_range = line.index("range:(") + len("range:(")
                end_range = line.index(")", start_range)
                ranges = line[start_range:end_range].split(',')
                
                # 將 range 值轉為數字並打印
                range_values = list(map(int, ranges))
                print(f"Range values: {range_values}")
                
                if len(range_values) >= 3:
                    # 計算 T0 的座標
                    t0_x, t0_y = calculate_position(range_values[:3], anchors)
                    print(f"T0 的座標: ({t0_x}, {t0_y})")
                
            except Exception as e:
                print(f"解析錯誤: {e}")

def calculate_position(ranges, anchors):
    """
    使用三角測量計算 T0 的位置
    ranges: T0 到每個 Anchor 的距離列表
    anchors: 每個 Anchor 的座標列表
    """
    # 錨點的位置
    (x1, y1), (x2, y2), (x3, y3) = anchors

    r1, r2, r3 = ranges

    # 計算三角測量
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)

    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2

    # 解方程得到 x 和 y
    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)

    return max(x, 0), max(y, 0)  # 防止負座標

def main():
    # 列出所有可用的 COM 端口
    available_ports = list_available_com_ports()
    if available_ports is None:
        return

    # 檢查輸入的 COM 端口是否在可用端口列表中
    if com_port not in [port.device for port in available_ports]:
        print(f"無法找到指定的端口: {com_port}")
        return

    # 設置 Anchor 座標
    anchors = [
        (0, 0),         # A0
        (0, 180),       # A1
        (120, 180),     # A2
    ]

    try:
        # 打開指定的COM端口
        ser = serial.Serial(com_port, 115200, timeout=1)  # 設置串列通信的端口和波特率
        time.sleep(2)  # 延遲等待 ESP32 準備
        ser.write("begin".encode())  # 發送命令讓 ESP32 開始回傳數據
        ser.reset_input_buffer()  # 清空串列緩衝區
        read_esp32_data(ser, anchors)  # 持續讀取 ESP32 回傳的數據

    except serial.SerialException as e:
        print(f"無法打開端口 {com_port}: {e}")
    except KeyboardInterrupt:
        print("停止讀取")
    finally:
        ser.close()  # 結束時關閉串列端口

if __name__ == "__main__":
    main()
