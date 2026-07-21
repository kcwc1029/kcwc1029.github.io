import barcode
from barcode.writer import ImageWriter
from pathlib import Path

current_dir = Path(__file__).resolve().parent
output_dir = current_dir.parent / "Qrcode_outputs"

output_dir.mkdir(parents=True, exist_ok=True)

EAN = barcode.get_barcode_class("ean13")

barcode_image = EAN(
    "5901234123457",
    writer=ImageWriter()
)

barcode_image.save(str(output_dir / "my_barcode_png"))

print("條碼建立完成")