"""API Requests 教材共用設定與小工具。"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "API_Requests_datasets" / "臺灣生活好物API資料.csv"
OUTPUT_DIR = PROJECT_DIR / "API_Requests_outputs"
BASE_URL = "http://127.0.0.1:8765/api/v1"


def prepare_output() -> None:
    """建立輸出資料夾。"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

