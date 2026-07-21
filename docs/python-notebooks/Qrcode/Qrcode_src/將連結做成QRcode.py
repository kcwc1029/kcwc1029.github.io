from pathlib import Path
import qrcode
from PIL import Image


# QRCode 內容
code_text = "https://jiashuo.com.tw/new/index.php?mode=&ver=tw&portal=jiashuo"

# 製作QRcode
img = qrcode.make(code_text)

# 儲存圖片
# img.save("school_qrcode.png")

# 開啟圖片
img.show()