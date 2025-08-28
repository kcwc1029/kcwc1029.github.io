import network
import config
import time
from machine import Pin
import gc
import urequests  # 使用 urequests 代替 xrequests

def connect_wifi_led(ssid, passwd, timeout=15):
    """
    使用 LED 指示燈連接到指定的 Wi-Fi 網路。

    :param ssid: Wi-Fi 的 SSID（網路名稱）
    :param passwd: Wi-Fi 密碼
    :param timeout: 嘗試連接的超時時間（秒），默認為15秒
    :return: 如果連接成功，返回設備的 IP 地址；如果超時，返回 None
    """
    # 初始化連接狀態的 LED（Pin 2）
    wifi_led = Pin(2, Pin.OUT, value=1)  # 預設 LED 為熄滅狀態（1）

    # 創建並啟用 STA 模式（Station 模式，用於連接 Wi-Fi）
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    # 紀錄連接開始時間，用於判斷是否超時
    start_time = time.time()

    # 如果尚未連接到 Wi-Fi
    if not sta.isconnected():
        print("Connecting to network...")  # 提示正在連接 Wi-Fi
        sta.connect(ssid, passwd)  # 發起連接請求

        # 等待 Wi-Fi 連接成功，或直到超時
        while not sta.isconnected():
            # LED 閃爍（表示正在嘗試連接）
            wifi_led.value(0)  # 開燈
            time.sleep_ms(300)
            wifi_led.value(1)  # 關燈
            time.sleep_ms(300)

            # 判斷是否超過設定的超時時間
            if time.time() - start_time > timeout:
                print("Wi-Fi connecting timeout!")  # 提示連接超時
                break

    # 如果成功連接到 Wi-Fi
    if sta.isconnected():
        wifi_led.value(0)  # 連接成功後關閉 LED
        print("Network config:", sta.ifconfig())  # 打印網路配置信息
        return sta.ifconfig()[0]  # 返回設備的 IP 地址

    # 如果超時或連接失敗
    return None

def webhook_post(url, value):
    print("invoking webhook")
    
    gc.collect()
    try:
        r = urequests.post(url, json=value)  # 使用 urequests.post，並傳遞 JSON 數據
        if r is not None and r.status_code == 200:
            print("Webhook invoked")
        else:
            print("Webhook failed")
    except Exception as e:
        print("Exception in POST:", e)

def webhook_get(url):
    print("invoking webhook")
    gc.collect()
    try:
        r = urequests.get(url)  # 使用 urequests.get
        if r is not None and r.status_code == 200:
            print("Webhook invoked")
        else:
            print("Webhook failed")
    except Exception as e:
        print("Exception in GET:", e)

if __name__ == "__main__":
    ip = connect_wifi_led(ssid=config.WIFI_SSID, passwd=config.WIFI_PASSWORD, timeout=15)
    print(ip)

