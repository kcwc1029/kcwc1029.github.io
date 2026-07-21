"""
咖啡店 POS 系統 — CustomTkinter
功能：
  • 菜單點餐（4 大類）
  • 品項備註（少冰、加糖…）
  • 折扣輸入（% 或固定金額）
  • 收款 / 找零計算
  • 結帳後跳出收據視窗
  • 交易紀錄自動存入 ./POS紀錄/<日期>.txt
  • 程式內查看今日紀錄
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os, re

# ── 主題 ─────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

C = {
    "bg":      "#14100e",
    "panel":   "#1e1812",
    "card":    "#252015",
    "border":  "#3a3020",
    "accent":  "#c8924a",   # 咖啡金
    "accent2": "#e8b86d",
    "green":   "#5dba7a",
    "red":     "#d9534f",
    "text":    "#f0e8d8",
    "sub":     "#9a8a70",
    "tag":     "#3a2a18",
}

FONT_H  = ("Georgia",    16, "bold")
FONT_M  = ("Georgia",    13)
FONT_S  = ("Consolas",   12)
FONT_XS = ("Consolas",   11)

# ── 菜單資料 ──────────────────────────────────────────────
MENU: dict[str, list[tuple[str, int]]] = {
    "☕ 手沖系列": [
        ("手沖咖啡 A", 65),
        ("手沖咖啡 B", 45),
        ("手沖咖啡 C", 50),
    ],
    "🥛 拿鐵系列": [
        ("拿鐵系列 A",  90),
        ("拿鐵系列 B", 120),
        ("拿鐵系列 C",  90),
    ],
    "🍰 甜點系列": [
        ("提拉米蘇", 130),
        ("肉桂捲",   130),
    ],
    "🥟 主食系列": [
        ("高麗菜水餃 (10顆)", 100),
        ("韭菜水餃 (10顆)",   100),
    ],
}

QUICK_NOTES = ["少冰", "去冰", "熱的", "加糖", "少糖", "無糖", "加大", "外帶"]

RECORD_DIR = "POS紀錄"


# ═══════════════════════════════════════════════════════════
#  備註對話框
# ═══════════════════════════════════════════════════════════
class NoteDialog(ctk.CTkToplevel):
    def __init__(self, master, item_name: str, current_note: str = ""):
        super().__init__(master)
        self.title("備註")
        self.geometry("360x300")
        self.configure(fg_color=C["panel"])
        self.grab_set()
        self.result: str | None = None

        ctk.CTkLabel(self, text=f"備註：{item_name}",
                     font=FONT_H, text_color=C["accent2"]).pack(pady=(18, 8))

        # 快速標籤
        tag_frame = ctk.CTkFrame(self, fg_color="transparent")
        tag_frame.pack(fill="x", padx=20)
        for i, n in enumerate(QUICK_NOTES):
            ctk.CTkButton(tag_frame, text=n, width=64, height=26,
                          font=FONT_XS,
                          fg_color=C["tag"], hover_color=C["border"],
                          text_color=C["text"],
                          command=lambda v=n: self._append(v)
                          ).grid(row=i//4, column=i%4, padx=3, pady=3)

        self._entry = ctk.CTkEntry(self, placeholder_text="自由輸入…",
                                   font=FONT_S,
                                   fg_color=C["bg"], border_color=C["border"],
                                   text_color=C["text"])
        self._entry.pack(fill="x", padx=20, pady=(10, 0))
        if current_note:
            self._entry.insert(0, current_note)

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=14)
        ctk.CTkButton(btn_row, text="確認", width=90,
                      fg_color=C["accent"], hover_color=C["accent2"],
                      text_color="#fff", font=FONT_S,
                      command=self._confirm).pack(side="left", padx=6)
        ctk.CTkButton(btn_row, text="清除", width=90,
                      fg_color=C["border"], hover_color=C["red"],
                      text_color=C["text"], font=FONT_S,
                      command=self._clear).pack(side="left", padx=6)

    def _append(self, v: str):
        cur = self._entry.get().strip()
        self._entry.delete(0, "end")
        self._entry.insert(0, (cur + " " + v).strip())

    def _confirm(self):
        self.result = self._entry.get().strip()
        self.destroy()

    def _clear(self):
        self.result = ""
        self.destroy()


# ═══════════════════════════════════════════════════════════
#  收據視窗
# ═══════════════════════════════════════════════════════════
class ReceiptWindow(ctk.CTkToplevel):
    def __init__(self, master, order: list, discount_amt: int,
                 total: int, received: int, change: int, order_no: int):
        super().__init__(master)
        self.title("收據")
        self.geometry("380x540")
        self.configure(fg_color=C["panel"])
        self.grab_set()
        self._master_ref = master

        now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

        ctk.CTkLabel(self, text="☕  島嶼咖啡",
                     font=("Georgia", 22, "bold"),
                     text_color=C["accent2"]).pack(pady=(20, 2))
        ctk.CTkLabel(self, text=now, font=FONT_XS,
                     text_color=C["sub"]).pack()
        ctk.CTkLabel(self, text=f"訂單 #{order_no:04d}", font=FONT_XS,
                     text_color=C["sub"]).pack(pady=(0, 10))

        sep = lambda: ctk.CTkLabel(self, text="─"*42, font=("Consolas", 10),
                                    text_color=C["border"]).pack()
        sep()

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=160)
        scroll.pack(fill="x", padx=20)

        for item in order:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            note_str = f"  [{item['note']}]" if item['note'] else ""
            ctk.CTkLabel(row,
                         text=f"{item['name']}{note_str}  ×{item['qty']}",
                         font=FONT_XS, text_color=C["text"],
                         anchor="w").pack(side="left")
            ctk.CTkLabel(row,
                         text=f"${item['price']*item['qty']}",
                         font=FONT_XS, text_color=C["text"],
                         anchor="e").pack(side="right")

        sep()

        def info_row(label, value, color=None):
            r = ctk.CTkFrame(self, fg_color="transparent")
            r.pack(fill="x", padx=24, pady=1)
            ctk.CTkLabel(r, text=label, font=FONT_S,
                         text_color=C["sub"]).pack(side="left")
            ctk.CTkLabel(r, text=value, font=FONT_S,
                         text_color=color or C["text"]).pack(side="right")

        subtotal = sum(i["price"]*i["qty"] for i in order)
        info_row("小計", f"${subtotal}")
        if discount_amt:
            info_row("折扣", f"-${discount_amt}", C["green"])
        info_row("總計", f"${total}", C["accent2"])
        info_row("收款", f"${received}")
        info_row("找零", f"${change}", C["green"])

        sep()

        ctk.CTkLabel(self, text="謝謝光臨  歡迎再來 ☕",
                     font=FONT_M, text_color=C["sub"]).pack(pady=8)

        ctk.CTkButton(self, text="關閉並清空訂單",
                      font=FONT_S,
                      fg_color=C["accent"], hover_color=C["accent2"],
                      text_color="#fff",
                      command=self._close).pack(pady=(4, 20))

    def _close(self):
        self._master_ref.clear_order()
        self.destroy()


# ═══════════════════════════════════════════════════════════
#  今日紀錄視窗
# ═══════════════════════════════════════════════════════════
class LogWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("今日交易紀錄")
        self.geometry("640x480")
        self.configure(fg_color=C["panel"])

        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(RECORD_DIR, f"{today}.txt")

        ctk.CTkLabel(self, text=f"📋  {today} 交易紀錄",
                     font=FONT_H, text_color=C["accent2"]).pack(pady=(16, 8))

        box = ctk.CTkTextbox(self, font=("Consolas", 11),
                             fg_color=C["bg"],
                             text_color=C["text"],
                             border_color=C["border"],
                             wrap="none")
        box.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
            box.insert("end", content)
        else:
            box.insert("end", "（今日尚無交易紀錄）")
        box.configure(state="disabled")


# ═══════════════════════════════════════════════════════════
#  主視窗
# ═══════════════════════════════════════════════════════════
class POSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("島嶼咖啡 POS")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(fg_color=C["bg"])

        os.makedirs(RECORD_DIR, exist_ok=True)

        # 訂單資料  {name: {price, qty, note}}
        self._order: dict[str, dict] = {}
        self._order_no = self._load_order_no()

        self._build()

    # ── 訂單號碼 ─────────────────────────────────────────
    def _load_order_no(self) -> int:
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(RECORD_DIR, f"{today}.txt")
        if not os.path.exists(path):
            return 0
        with open(path, encoding="utf-8") as f:
            lines = [l for l in f.readlines() if l.strip()]
        return len(lines)

    # ── 建構 UI ──────────────────────────────────────────
    def _build(self):
        # 頂欄
        topbar = ctk.CTkFrame(self, fg_color=C["panel"],
                               corner_radius=0, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="☕  島嶼咖啡 POS",
                     font=("Georgia", 18, "bold"),
                     text_color=C["accent2"]).pack(side="left", padx=20)

        ctk.CTkButton(topbar, text="📋 今日紀錄", width=110, height=32,
                      font=FONT_XS,
                      fg_color=C["tag"], hover_color=C["border"],
                      text_color=C["text"],
                      command=lambda: LogWindow(self)).pack(side="right", padx=12)

        now_label = ctk.CTkLabel(topbar, text="", font=FONT_XS,
                                  text_color=C["sub"])
        now_label.pack(side="right", padx=8)
        self._clock_label = now_label
        self._tick_clock()

        # 主體：左（菜單）＋ 右（訂單）
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=12, pady=10)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        self._build_menu(body)
        self._build_order(body)

    # ── 時鐘 ─────────────────────────────────────────────
    def _tick_clock(self):
        self._clock_label.configure(
            text=datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        self.after(1000, self._tick_clock)

    # ── 左側菜單 ─────────────────────────────────────────
    def _build_menu(self, parent):
        frame = ctk.CTkScrollableFrame(parent, fg_color="transparent",
                                        scrollbar_button_color=C["border"])
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        for category, items in MENU.items():
            # 分類標題
            ctk.CTkLabel(frame, text=category,
                         font=("Georgia", 15, "bold"),
                         text_color=C["accent"],
                         anchor="w").pack(fill="x", padx=4, pady=(14, 4))

            grid = ctk.CTkFrame(frame, fg_color="transparent")
            grid.pack(fill="x", padx=4)

            for idx, (name, price) in enumerate(items):
                card = ctk.CTkFrame(grid, fg_color=C["card"],
                                    corner_radius=10,
                                    border_width=1, border_color=C["border"])
                card.grid(row=idx//3, column=idx%3,
                          padx=5, pady=5, sticky="ew")
                grid.columnconfigure(idx%3, weight=1)

                ctk.CTkLabel(card, text=name,
                             font=FONT_S, text_color=C["text"],
                             wraplength=130, justify="center").pack(pady=(12, 2))
                ctk.CTkLabel(card, text=f"${price}",
                             font=("Georgia", 14, "bold"),
                             text_color=C["accent2"]).pack(pady=(0, 8))

                btn_row = ctk.CTkFrame(card, fg_color="transparent")
                btn_row.pack(pady=(0, 10))

                ctk.CTkButton(btn_row, text="＋", width=36, height=30,
                              font=("Consolas", 14, "bold"),
                              fg_color=C["accent"], hover_color=C["accent2"],
                              text_color="#fff",
                              command=lambda n=name, p=price: self._add(n, p)
                              ).pack(side="left", padx=2)
                ctk.CTkButton(btn_row, text="備註", width=46, height=30,
                              font=FONT_XS,
                              fg_color=C["tag"], hover_color=C["border"],
                              text_color=C["text"],
                              command=lambda n=name, p=price: self._open_note(n, p)
                              ).pack(side="left", padx=2)

    # ── 右側訂單 ─────────────────────────────────────────
    def _build_order(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=C["panel"],
                              corner_radius=12,
                              border_width=1, border_color=C["border"])
        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="訂單",
                     font=FONT_H, text_color=C["accent2"]).grid(
            row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        # 訂單列表
        self._order_scroll = ctk.CTkScrollableFrame(
            frame, fg_color="transparent",
            scrollbar_button_color=C["border"])
        self._order_scroll.grid(row=1, column=0, sticky="nsew", padx=10)
        frame.columnconfigure(0, weight=1)

        self._order_rows: dict[str, ctk.CTkFrame] = {}

        # ── 折扣區 ───────────────────────────────────────
        disc_frame = ctk.CTkFrame(frame, fg_color=C["card"],
                                   corner_radius=8)
        disc_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(6, 0))

        ctk.CTkLabel(disc_frame, text="折扣",
                     font=FONT_XS, text_color=C["sub"]).grid(
            row=0, column=0, padx=10, pady=6, sticky="w")

        self._disc_var  = ctk.StringVar(value="")
        self._disc_type = ctk.StringVar(value="amount")

        ctk.CTkEntry(disc_frame, textvariable=self._disc_var,
                     placeholder_text="輸入折扣…",
                     width=100, font=FONT_S,
                     fg_color=C["bg"], border_color=C["border"],
                     text_color=C["text"]).grid(row=0, column=1, padx=4)

        ctk.CTkRadioButton(disc_frame, text="固定 $",
                           variable=self._disc_type, value="amount",
                           font=FONT_XS, text_color=C["text"]).grid(
            row=0, column=2, padx=4)
        ctk.CTkRadioButton(disc_frame, text="百分比 %",
                           variable=self._disc_type, value="percent",
                           font=FONT_XS, text_color=C["text"]).grid(
            row=0, column=3, padx=4)

        # ── 收款區 ───────────────────────────────────────
        pay_frame = ctk.CTkFrame(frame, fg_color=C["card"], corner_radius=8)
        pay_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=6)

        ctk.CTkLabel(pay_frame, text="小計", font=FONT_XS,
                     text_color=C["sub"]).grid(row=0, column=0, padx=10, pady=4, sticky="w")
        self._subtotal_lbl = ctk.CTkLabel(pay_frame, text="$0",
                                           font=FONT_S, text_color=C["text"])
        self._subtotal_lbl.grid(row=0, column=1, sticky="e", padx=10)

        ctk.CTkLabel(pay_frame, text="折扣後", font=FONT_XS,
                     text_color=C["sub"]).grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self._total_lbl = ctk.CTkLabel(pay_frame, text="$0",
                                        font=("Georgia", 15, "bold"),
                                        text_color=C["accent2"])
        self._total_lbl.grid(row=1, column=1, sticky="e", padx=10)

        pay_frame.columnconfigure(1, weight=1)

        recv_row = ctk.CTkFrame(pay_frame, fg_color="transparent")
        recv_row.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(4, 8))

        ctk.CTkLabel(recv_row, text="收款 $",
                     font=FONT_S, text_color=C["text"]).pack(side="left")
        self._recv_entry = ctk.CTkEntry(recv_row, width=90, font=FONT_S,
                                         fg_color=C["bg"],
                                         border_color=C["border"],
                                         text_color=C["text"],
                                         placeholder_text="0")
        self._recv_entry.pack(side="left", padx=6)
        self._recv_entry.bind("<KeyRelease>", lambda e: self._refresh_change())

        ctk.CTkLabel(recv_row, text="找零",
                     font=FONT_S, text_color=C["sub"]).pack(side="left", padx=(12, 4))
        self._change_lbl = ctk.CTkLabel(recv_row, text="$—",
                                         font=("Georgia", 14, "bold"),
                                         text_color=C["green"])
        self._change_lbl.pack(side="left")

        # ── 操作按鈕 ─────────────────────────────────────
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, pady=(0, 12))

        ctk.CTkButton(btn_frame, text="結帳", width=120, height=40,
                      font=("Georgia", 14, "bold"),
                      fg_color=C["accent"], hover_color=C["accent2"],
                      text_color="#fff",
                      command=self._checkout).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="清空訂單", width=100, height=40,
                      font=FONT_S,
                      fg_color=C["border"], hover_color=C["red"],
                      text_color=C["text"],
                      command=self.clear_order).pack(side="left", padx=6)

    # ── 加入品項 ─────────────────────────────────────────
    def _add(self, name: str, price: int, note: str = ""):
        if name in self._order:
            self._order[name]["qty"] += 1
            self._update_row(name)
        else:
            self._order[name] = {"price": price, "qty": 1, "note": note}
            self._add_row(name)
        self._refresh_total()

    def _open_note(self, name: str, price: int):
        cur_note = self._order.get(name, {}).get("note", "")
        dlg = NoteDialog(self, name, cur_note)
        self.wait_window(dlg)
        if dlg.result is not None:
            if name not in self._order:
                self._order[name] = {"price": price, "qty": 1, "note": dlg.result}
                self._add_row(name)
            else:
                self._order[name]["note"] = dlg.result
                self._update_row(name)
            self._refresh_total()

    # ── 訂單 Row ─────────────────────────────────────────
    def _add_row(self, name: str):
        row = ctk.CTkFrame(self._order_scroll, fg_color=C["card"],
                            corner_radius=8)
        row.pack(fill="x", pady=3)
        self._order_rows[name] = row
        self._render_row(name)

    def _update_row(self, name: str):
        row = self._order_rows[name]
        for w in row.winfo_children():
            w.destroy()
        self._render_row(name)

    def _render_row(self, name: str):
        item = self._order[name]
        row  = self._order_rows[name]

        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(fill="x", padx=8, pady=(6, 0))

        ctk.CTkLabel(info, text=name, font=FONT_S,
                     text_color=C["text"], anchor="w").pack(side="left")
        ctk.CTkLabel(info, text=f"${item['price'] * item['qty']}",
                     font=("Georgia", 13, "bold"),
                     text_color=C["accent2"]).pack(side="right")

        ctrl = ctk.CTkFrame(row, fg_color="transparent")
        ctrl.pack(fill="x", padx=8, pady=(2, 6))

        # note
        note_text = item["note"] if item["note"] else "無備註"
        note_color = C["accent"] if item["note"] else C["sub"]
        ctk.CTkLabel(ctrl, text=note_text, font=FONT_XS,
                     text_color=note_color).pack(side="left")

        # qty controls
        qty_box = ctk.CTkFrame(ctrl, fg_color="transparent")
        qty_box.pack(side="right")

        ctk.CTkButton(qty_box, text="−", width=26, height=24,
                      font=("Consolas", 13, "bold"),
                      fg_color=C["border"], hover_color=C["red"],
                      text_color=C["text"],
                      command=lambda n=name: self._dec(n)
                      ).pack(side="left", padx=1)
        ctk.CTkLabel(qty_box, text=str(item["qty"]),
                     width=28, font=FONT_S,
                     text_color=C["text"]).pack(side="left")
        ctk.CTkButton(qty_box, text="＋", width=26, height=24,
                      font=("Consolas", 13, "bold"),
                      fg_color=C["accent"], hover_color=C["accent2"],
                      text_color="#fff",
                      command=lambda n=name: self._inc(n)
                      ).pack(side="left", padx=1)

    def _inc(self, name: str):
        self._order[name]["qty"] += 1
        self._update_row(name)
        self._refresh_total()

    def _dec(self, name: str):
        self._order[name]["qty"] -= 1
        if self._order[name]["qty"] <= 0:
            self._order_rows[name].destroy()
            del self._order_rows[name]
            del self._order[name]
        else:
            self._update_row(name)
        self._refresh_total()

    # ── 金額計算 ─────────────────────────────────────────
    def _calc_discount(self, subtotal: int) -> int:
        raw = self._disc_var.get().strip()
        if not raw:
            return 0
        try:
            v = float(raw)
        except ValueError:
            return 0
        if self._disc_type.get() == "percent":
            return int(subtotal * v / 100)
        return int(v)

    def _refresh_total(self):
        subtotal = sum(i["price"] * i["qty"] for i in self._order.values())
        disc     = self._calc_discount(subtotal)
        total    = max(0, subtotal - disc)
        self._subtotal_lbl.configure(text=f"${subtotal}")
        self._total_lbl.configure(text=f"${total}")
        self._refresh_change()

    def _refresh_change(self):
        subtotal = sum(i["price"] * i["qty"] for i in self._order.values())
        disc     = self._calc_discount(subtotal)
        total    = max(0, subtotal - disc)
        try:
            recv   = int(self._recv_entry.get())
            change = recv - total
            color  = C["green"] if change >= 0 else C["red"]
            self._change_lbl.configure(text=f"${change}", text_color=color)
        except ValueError:
            self._change_lbl.configure(text="$—", text_color=C["green"])

    # ── 結帳 ─────────────────────────────────────────────
    def _checkout(self):
        if not self._order:
            messagebox.showwarning("訂單空白", "請先加入品項！")
            return

        subtotal = sum(i["price"] * i["qty"] for i in self._order.values())
        disc     = self._calc_discount(subtotal)
        total    = max(0, subtotal - disc)

        try:
            recv = int(self._recv_entry.get())
        except ValueError:
            messagebox.showwarning("收款金額", "請輸入收款金額！")
            return

        if recv < total:
            messagebox.showwarning("收款不足", f"收款 ${recv} 不足總計 ${total}！")
            return

        change = recv - total
        self._order_no += 1

        # 寫入紀錄
        self._write_record(subtotal, disc, total, recv, change)

        # 整理 order list
        order_list = [
            {"name": n, "price": d["price"], "qty": d["qty"], "note": d["note"]}
            for n, d in self._order.items()
        ]

        ReceiptWindow(self, order_list, disc, total, recv, change, self._order_no)

    # ── 寫入 TXT ─────────────────────────────────────────
    def _write_record(self, subtotal, disc, total, recv, change):
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(RECORD_DIR, f"{today}.txt")
        now   = datetime.now().strftime("%H:%M:%S")

        items_str = "、".join(
            f"{n}×{d['qty']}" + (f"({d['note']})" if d["note"] else "")
            for n, d in self._order.items()
        )
        disc_str = f" 折扣-{disc}" if disc else ""
        line = (f"[#{self._order_no:04d}] {now}  "
                f"{items_str}  "
                f"小計${subtotal}{disc_str}  總計${total}  "
                f"收款${recv}  找零${change}\n")

        with open(path, "a", encoding="utf-8") as f:
            f.write(line)

    # ── 清空 ─────────────────────────────────────────────
    def clear_order(self):
        for row in self._order_rows.values():
            row.destroy()
        self._order_rows.clear()
        self._order.clear()
        self._recv_entry.delete(0, "end")
        self._disc_var.set("")
        self._subtotal_lbl.configure(text="$0")
        self._total_lbl.configure(text="$0")
        self._change_lbl.configure(text="$—")


if __name__ == "__main__":
    app = POSApp()
    app.mainloop()