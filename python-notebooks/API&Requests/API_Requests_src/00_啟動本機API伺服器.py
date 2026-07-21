"""啟動職訓課程專用 REST API；只監聽本機 127.0.0.1。"""

import csv
import hashlib
import json
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from api_utils import DATA_FILE


def load_products() -> list[dict]:
    """載入 72 筆商品，將 CSV 文字轉為 API 需要的數字與布林值。"""
    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    products = []
    for row in rows:
        products.append({
            "id": row["商品編號"],
            "name": row["商品名稱"],
            "category": row["分類"],
            "brand": row["品牌"],
            "price": int(row["價格"]),
            "original_price": int(row["原價"]),
            "rating": float(row["評分"]),
            "review_count": int(row["評論數"]),
            "stock": int(row["庫存"]),
            "ship_from": row["出貨地"],
            "free_shipping": row["免運"] == "是",
            "tag": row["標籤"],
        })
    return products


PRODUCTS = load_products()
TASKS = [
    {"id": 1, "title": "閱讀 API 文件", "completed": True, "priority": "高"},
    {"id": 2, "title": "完成 Requests 練習", "completed": False, "priority": "高"},
    {"id": 3, "title": "整理作品集說明", "completed": False, "priority": "中"},
]
ORDERS_BY_KEY: dict[str, dict] = {}
VALID_TOKEN = "training-demo-token"


class ApiHandler(BaseHTTPRequestHandler):
    """不依賴第三方 Web 框架的教學 API。"""

    server_version = "ApiRequestsCourse/2.0"

    def send_json(self, data: object, status: int = 200, headers: dict | None = None) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-API-Version", "v1")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict | None:
        """讀取 JSON body；格式錯誤時直接回傳 400。"""
        length = int(self.headers.get("Content-Length", "0"))
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json({"error": {"code": "INVALID_JSON", "message": "JSON 格式錯誤"}}, 400)
            return None

    def is_authorized(self) -> bool:
        if self.headers.get("Authorization") != f"Bearer {VALID_TOKEN}":
            self.send_json(
                {"error": {"code": "UNAUTHORIZED", "message": "請提供有效的 Bearer Token"}},
                HTTPStatus.UNAUTHORIZED,
                {"WWW-Authenticate": "Bearer"},
            )
            return False
        return True

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        path = parsed.path.rstrip("/")

        if path == "/api/v1/health":
            self.send_json({"status": "ok", "service": "API Requests 教學服務", "version": "1.0.0"})
            return

        if path == "/api/v1/slow":
            time.sleep(min(float(query.get("seconds", ["2"])[0]), 8))
            self.send_json({"message": "延遲回應完成"})
            return

        if path == "/api/v1/products":
            try:
                page = max(int(query.get("page", ["1"])[0]), 1)
                per_page = min(max(int(query.get("per_page", ["10"])[0]), 1), 30)
                min_price = int(query.get("min_price", ["0"])[0])
                max_price = int(query.get("max_price", ["999999"])[0])
            except ValueError:
                self.send_json({"error": {"code": "INVALID_PARAMETER", "message": "分頁與價格必須是整數"}}, 400)
                return
            category = query.get("category", [""])[0]
            keyword = query.get("q", [""])[0].lower()
            sort = query.get("sort", ["id"])[0]
            items = [item for item in PRODUCTS if min_price <= item["price"] <= max_price]
            if category:
                items = [item for item in items if item["category"] == category]
            if keyword:
                items = [item for item in items if keyword in item["name"].lower()]
            sort_map = {"id": "id", "price": "price", "rating": "rating", "reviews": "review_count"}
            if sort.lstrip("-") not in sort_map:
                self.send_json({"error": {"code": "INVALID_SORT", "message": "不支援的排序欄位"}}, 400)
                return
            items.sort(key=lambda item: item[sort_map[sort.lstrip("-")]], reverse=sort.startswith("-"))
            start = (page - 1) * per_page
            page_items = items[start:start + per_page]
            self.send_json({
                "data": page_items,
                "meta": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(items),
                    "total_pages": (len(items) + per_page - 1) // per_page,
                    "has_next": start + per_page < len(items),
                },
            })
            return

        if path.startswith("/api/v1/products/"):
            product_id = path.rsplit("/", 1)[-1]
            product = next((item for item in PRODUCTS if item["id"] == product_id), None)
            if product is None:
                self.send_json({"error": {"code": "NOT_FOUND", "message": "查無此商品"}}, 404)
            else:
                self.send_json({"data": product})
            return

        if path == "/api/v1/tasks":
            if self.is_authorized():
                self.send_json({"data": TASKS, "meta": {"total": len(TASKS)}})
            return

        if path == "/api/v1/products-summary":
            summary = {
                "product_count": len(PRODUCTS),
                "in_stock_count": sum(item["stock"] > 0 for item in PRODUCTS),
                "average_price": round(sum(item["price"] for item in PRODUCTS) / len(PRODUCTS), 2),
            }
            body_for_hash = json.dumps(summary, sort_keys=True).encode()
            etag = '"' + hashlib.sha256(body_for_hash).hexdigest()[:16] + '"'
            if self.headers.get("If-None-Match") == etag:
                self.send_response(HTTPStatus.NOT_MODIFIED)
                self.send_header("ETag", etag)
                self.end_headers()
            else:
                self.send_json({"data": summary}, headers={"ETag": etag, "Cache-Control": "max-age=60"})
            return

        if path == "/api/v1/products.csv":
            body = DATA_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Content-Disposition", 'attachment; filename="products.csv"')
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_json({"error": {"code": "NOT_FOUND", "message": "API 路徑不存在"}}, 404)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path.rstrip("/")
        data = self.read_json()
        if data is None:
            return

        if path == "/api/v1/auth/token":
            if data.get("username") == "student" and data.get("password") == "python123":
                self.send_json({"access_token": VALID_TOKEN, "token_type": "Bearer", "expires_in": 3600})
            else:
                self.send_json({"error": {"code": "INVALID_CREDENTIALS", "message": "帳號或密碼錯誤"}}, 401)
            return

        if path == "/api/v1/orders":
            if not self.is_authorized():
                return
            idempotency_key = self.headers.get("Idempotency-Key")
            if not idempotency_key:
                self.send_json({"error": {"code": "MISSING_IDEMPOTENCY_KEY", "message": "缺少 Idempotency-Key"}}, 400)
                return
            if idempotency_key in ORDERS_BY_KEY:
                self.send_json({"data": ORDERS_BY_KEY[idempotency_key], "replayed": True})
                return
            if not isinstance(data.get("items"), list) or not data["items"]:
                self.send_json({"error": {"code": "VALIDATION_ERROR", "message": "items 必須是非空陣列"}}, 422)
                return
            order = {"id": f"O-{uuid.uuid4().hex[:8].upper()}", "status": "created", "items": data["items"]}
            ORDERS_BY_KEY[idempotency_key] = order
            self.send_json({"data": order, "replayed": False}, HTTPStatus.CREATED, {"Location": f'/api/v1/orders/{order["id"]}'})
            return

        if path == "/api/v1/tasks":
            if not self.is_authorized():
                return
            title = str(data.get("title", "")).strip()
            if not title:
                self.send_json({"error": {"code": "VALIDATION_ERROR", "message": "title 不可空白"}}, 422)
                return
            task = {"id": max((task["id"] for task in TASKS), default=0) + 1, "title": title, "completed": False, "priority": data.get("priority", "中")}
            TASKS.append(task)
            self.send_json({"data": task}, HTTPStatus.CREATED, {"Location": f'/api/v1/tasks/{task["id"]}'})
            return

        self.send_json({"error": {"code": "NOT_FOUND", "message": "API 路徑不存在"}}, 404)

    def do_PUT(self) -> None:  # noqa: N802
        self.update_task(replace=True)

    def do_PATCH(self) -> None:  # noqa: N802
        self.update_task(replace=False)

    def update_task(self, replace: bool) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if not path.startswith("/api/v1/tasks/"):
            self.send_json({"error": {"code": "NOT_FOUND", "message": "API 路徑不存在"}}, 404)
            return
        if not self.is_authorized():
            return
        data = self.read_json()
        if data is None:
            return
        try:
            task_id = int(path.rsplit("/", 1)[-1])
        except ValueError:
            self.send_json({"error": {"code": "INVALID_ID", "message": "任務 ID 格式錯誤"}}, 400)
            return
        task = next((item for item in TASKS if item["id"] == task_id), None)
        if task is None:
            self.send_json({"error": {"code": "NOT_FOUND", "message": "查無任務"}}, 404)
            return
        if replace:
            required = {"title", "completed", "priority"}
            if not required.issubset(data):
                self.send_json({"error": {"code": "VALIDATION_ERROR", "message": "PUT 必須提供完整欄位"}}, 422)
                return
            task.update({key: data[key] for key in required})
        else:
            task.update({key: value for key, value in data.items() if key in {"title", "completed", "priority"}})
        self.send_json({"data": task})

    def do_DELETE(self) -> None:  # noqa: N802
        path = urlparse(self.path).path.rstrip("/")
        if not path.startswith("/api/v1/tasks/"):
            self.send_json({"error": {"code": "NOT_FOUND", "message": "API 路徑不存在"}}, 404)
            return
        if not self.is_authorized():
            return
        try:
            task_id = int(path.rsplit("/", 1)[-1])
        except ValueError:
            self.send_json({"error": {"code": "INVALID_ID", "message": "任務 ID 格式錯誤"}}, 400)
            return
        index = next((i for i, task in enumerate(TASKS) if task["id"] == task_id), None)
        if index is None:
            self.send_json({"error": {"code": "NOT_FOUND", "message": "查無任務"}}, 404)
            return
        TASKS.pop(index)
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        print(f"[API] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), ApiHandler)
    print("本機 API 已啟動：http://127.0.0.1:8765/api/v1")
    print("請保留此終端機，按 Ctrl+C 可停止。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAPI 已停止。")
    finally:
        server.server_close()
