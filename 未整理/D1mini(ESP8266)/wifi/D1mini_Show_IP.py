import network
import ubinascii

sta = network.WLAN(network.STA_IF)  # 創建 STA 模式的 WLAN 物件 (Station模式)
sta.active(True)  # 啟用 WLAN
print("當前開發版是否已經連上網路：", sta.isconnected())  # 檢查是否已連接到 Wi-Fi 網絡
print("----------")

aps = sta.scan()  # 掃描附近的 Wi-Fi 熱點
for ap in aps:  # 遍歷掃描結果
    ssid = ap[0].decode()  # 提取 SSID（網絡名稱），並將 bytes 解碼為字串
    mac = ubinascii.hexlify(ap[1], ":").decode()  # 提取 BSSID（MAC 位址），轉換為可讀格式
    print(ssid, mac)  # 打印 SSID 和 MAC 位址

# 輸出
# MPY: soft reboot
# 當前開發版是否已經連上網路： False
# ----------
# MCAS_Lab fc:34:97:d1:f4:10
# 41112 7c:10:c9:e0:86:38
# guest_2.4G fc:34:97:2a:dd:51
#  62:83:e7:29:d2:da
# 16-3A f8:1d:0f:47:51:18
# PASI_LAB c8:3a:35:3b:e4:20
# gedlab_2G a8:5e:45:09:6f:40
# yucheng fc:34:97:2a:e1:31
# ALHC_Lab c8:78:7d:e6:ac:84
# ALHC-guest ca:78:7d:e6:ac:84