import network
import time

# 連接到指定的 Wi-Fi 熱點。
def connect_to_wifi(ssid, password, timeout=10):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if not sta.isconnected():
        print("嘗試連接到 Wi-Fi...")
        sta.connect(ssid, password)

        start_time = time.time()
        while not sta.isconnected():
            if time.time() - start_time > timeout:
                print("連接超時，請檢查 SSID 和密碼是否正確。")
                return None
            time.sleep(0.5)
    print("成功連接到 Wi-Fi!")
    return sta.ifconfig()

def disconnect_from_wifi():
    """
    斷開 Wi-Fi 連接。
    返回：
        bool: 返回是否仍然保持連接（True 表示連接，False 表示已斷開）。
    """
    sta = network.WLAN(network.STA_IF)
    if sta.isconnected():
        sta.disconnect()
        print("已斷開 Wi-Fi 連線。")
    else:
        print("目前無 Wi-Fi 連線。")
    return sta.isconnected()


if __name__ == "__main__":
    ssid = "ALHC-guest"
    password = "ALHCguest"
    # 連接到 Wi-Fi
    config = connect_to_wifi(ssid, password, timeout=10)
    if config:
        # 輸出：IP、mask、Gateway、DNS
        print("網絡配置:", config)
        time.sleep(3)

        # 斷開連線
        is_connected = disconnect_from_wifi()
        print("連線狀態:", is_connected)