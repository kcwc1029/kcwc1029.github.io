import connect_wifi
import config
import math
import urandom
import utime

class CFG:
    Key = "7OXRP61X5Z87K9MJ"



def random_in_range(low=0, high=1000):
    r1 = urandom.getrandbits(32)
    r2 = r1 % (high-low) + low
    return math.floor(r2)


if __name__ == "__main__":
    ip = connect_wifi.connect_wifi_led(ssid=config.WIFI_SSID, passwd=config.WIFI_PASSWORD, timeout=15)
    while True:
        temp  = random_in_range(10, 35)
        humidity  = random_in_range(60, 90)
        url = f"https://api.thingspeak.com/update?api_key={CFG.Key}&field1={temp}&field2={humidity}"
        connect_wifi.webhook_get(url)
        print(temp, humidity)
        utime.sleep(5)



