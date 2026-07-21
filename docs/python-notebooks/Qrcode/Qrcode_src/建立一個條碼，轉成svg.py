from pathlib import Path
import barcode


### 輸出資料夾路徑
# Path(__file__).resolve() 取得目前 Python 檔案的絕對路徑
# .parent 取得目前檔案所在資料夾
current_dir = Path(__file__).resolve().parent

# 回到上一層目錄後，組合 Qrcode_outputs 資料夾路徑
output_dir = current_dir.parent / "Qrcode_outputs"


### 建立 EAN13 條碼類別
EAN = barcode.get_barcode_class("ean13")


### 產生條碼物件
# EAN13 必須輸入 12 或 13 碼數字
# 若提供 12 碼，套件會自動計算檢查碼
# 此範例使用完整 13 碼條碼
svg_barcode = EAN("5901234123457")


### 儲存 SVG 條碼
# save() 不需要副檔名
# python-barcode 會自動產生 .svg 檔案
svg_barcode.save(
    str(output_dir / "my_barcode_svg")
)

print("SVG 條碼已產生完成！")