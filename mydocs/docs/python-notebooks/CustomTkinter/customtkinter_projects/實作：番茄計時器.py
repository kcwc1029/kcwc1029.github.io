番茄計時器"""
番茄計時器 — CustomTkinter
支援：
  • 同時設定多個計時器
  • 兩種模式：「幾分鐘後」/ 「指定時刻」
  • 自訂提醒文字
  • 時間到彈出通知視窗 + 系統通知（可選）
  • 開始 / 暫停 / 重置
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time, threading

# ── 全域主題 ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PALETTE = {
    "bg":       "#0d1117",
    "panel":    "#161b22",
    "border":   "#30363d",
    "accent":   "#58a6ff",
    "green":    "#3fb950",
    "orange":   "#f0883e",
    "red":      "#f85149",
    "text":     "#e6edf3",
    "subtext":  "#8b949e",
}

# ── 單一計時器卡片 ────────────────────────────────────────
class TimerCard(ctk.CTkFrame):
    CARD_ID = 0

    def __init__(self, master, on_remove, **kwargs):
        super().__init__(master, fg_color=PALETTE["panel"],
                         corner_radius=12, border_width=1,
                         border_color=PALETTE["border"], **kwargs)
        TimerCard.CARD_ID += 1
        self._id        = TimerCard.CARD_ID
        self._on_remove = on_remove
        self._running   = False
        self._paused    = False
        self._target_ts : float | None = None   # unix timestamp
        self._remaining : int   = 0             # seconds
        self._thread    : threading.Thread | None = None
        self._stop_evt  = threading.Event()

        self._build()

    # ── 建構 UI ──────────────────────────────────────────
    def _build(self):
        # 頂列：標題 + 刪除
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(12, 0))

        ctk.CTkLabel(top, text=f"計時器 #{self._id}",
                     font=("Consolas", 13, "bold"),
                     text_color=PALETTE["accent"]).pack(side="left")
        ctk.CTkButton(top, text="✕", width=28, height=28,
                      font=("Consolas", 13),
                      fg_color=PALETTE["border"], hover_color=PALETTE["red"],
                      text_color=PALETTE["text"],
                      command=self._remove).pack(side="right")

        # ── 模式選擇 ─────────────────────────────────────
        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.pack(fill="x", padx=14, pady=(8, 0))

        self._mode = ctk.StringVar(value="minutes")
        ctk.CTkRadioButton(mode_frame, text="幾分鐘後",
                           variable=self._mode, value="minutes",
                           font=("Consolas", 12),
                           text_color=PALETTE["text"],
                           command=self._mode_changed).pack(side="left", padx=(0,16))
        ctk.CTkRadioButton(mode_frame, text="指定時刻",
                           variable=self._mode, value="clock",
                           font=("Consolas", 12),
                           text_color=PALETTE["text"],
                           command=self._mode_changed).pack(side="left")

        # ── 輸入區（分鐘 / 時刻 切換） ───────────────────
        self._input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._input_frame.pack(fill="x", padx=14, pady=(6, 0))
        self._build_minute_input()

        # ── 提醒文字 ─────────────────────────────────────
        ctk.CTkLabel(self, text="提醒文字",
                     font=("Consolas", 11),
                     text_color=PALETTE["subtext"]).pack(anchor="w", padx=14, pady=(8,0))
        self._msg_entry = ctk.CTkEntry(self, placeholder_text="輸入提醒內容…",
                                       font=("Consolas", 12),
                                       fg_color=PALETTE["bg"],
                                       border_color=PALETTE["border"],
                                       text_color=PALETTE["text"])
        self._msg_entry.pack(fill="x", padx=14)

        # ── 倒數顯示 ─────────────────────────────────────
        self._countdown_label = ctk.CTkLabel(
            self, text="──:──:──",
            font=("Consolas", 36, "bold"),
            text_color=PALETTE["text"]
        )
        self._countdown_label.pack(pady=(10, 4))

        self._status_label = ctk.CTkLabel(
            self, text="待機中",
            font=("Consolas", 11),
            text_color=PALETTE["subtext"]
        )
        self._status_label.pack()

        # ── 控制按鈕 ─────────────────────────────────────
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(8, 14))

        btn_cfg = dict(width=80, height=34, corner_radius=8,
                       font=("Consolas", 12, "bold"))

        self._start_btn = ctk.CTkButton(btn_row, text="▶ 開始",
                                         fg_color=PALETTE["green"],
                                         hover_color="#2ea043",
                                         text_color="#fff",
                                         command=self._start, **btn_cfg)
        self._start_btn.pack(side="left", padx=4)

        self._pause_btn = ctk.CTkButton(btn_row, text="⏸ 暫停",
                                         fg_color=PALETTE["orange"],
                                         hover_color="#d08030",
                                         text_color="#fff",
                                         state="disabled",
                                         command=self._pause, **btn_cfg)
        self._pause_btn.pack(side="left", padx=4)

        self._reset_btn = ctk.CTkButton(btn_row, text="↺ 重置",
                                         fg_color=PALETTE["border"],
                                         hover_color="#484f58",
                                         text_color=PALETTE["text"],
                                         command=self._reset, **btn_cfg)
        self._reset_btn.pack(side="left", padx=4)

    # ── 模式輸入區 ───────────────────────────────────────
    def _clear_input_frame(self):
        for w in self._input_frame.winfo_children():
            w.destroy()

    def _build_minute_input(self):
        self._clear_input_frame()
        ctk.CTkLabel(self._input_frame, text="分鐘數",
                     font=("Consolas", 11),
                     text_color=PALETTE["subtext"]).pack(side="left", padx=(0,6))
        self._min_var = ctk.StringVar(value="25")
        vcmd = (self.register(lambda s: s.isdigit() or s == ""), "%P")
        self._min_entry = ctk.CTkEntry(self._input_frame,
                                        textvariable=self._min_var,
                                        width=72, font=("Consolas", 14),
                                        fg_color=PALETTE["bg"],
                                        border_color=PALETTE["border"],
                                        text_color=PALETTE["text"],
                                        validate="key", validatecommand=vcmd)
        self._min_entry.pack(side="left")
        ctk.CTkLabel(self._input_frame, text="分",
                     font=("Consolas", 11),
                     text_color=PALETTE["subtext"]).pack(side="left", padx=(4,0))

        # 快速按鈕
        for m in (5, 10, 25, 60):
            ctk.CTkButton(self._input_frame, text=f"+{m}",
                          width=36, height=26, corner_radius=6,
                          font=("Consolas", 11),
                          fg_color=PALETTE["border"],
                          hover_color="#484f58",
                          text_color=PALETTE["text"],
                          command=lambda v=m: self._add_minutes(v)
                          ).pack(side="left", padx=2)

    def _build_clock_input(self):
        self._clear_input_frame()
        ctk.CTkLabel(self._input_frame, text="時刻（HH:MM）",
                     font=("Consolas", 11),
                     text_color=PALETTE["subtext"]).pack(side="left", padx=(0,6))
        now = datetime.now().strftime("%H:%M")
        self._clock_var = ctk.StringVar(value=now)
        self._clock_entry = ctk.CTkEntry(self._input_frame,
                                          textvariable=self._clock_var,
                                          width=80, font=("Consolas", 14),
                                          fg_color=PALETTE["bg"],
                                          border_color=PALETTE["border"],
                                          text_color=PALETTE["text"],
                                          placeholder_text="09:30")
        self._clock_entry.pack(side="left")

    def _mode_changed(self):
        if self._mode.get() == "minutes":
            self._build_minute_input()
        else:
            self._build_clock_input()

    def _add_minutes(self, v):
        try:
            cur = int(self._min_var.get() or 0)
        except ValueError:
            cur = 0
        self._min_var.set(str(cur + v))

    # ── 計算目標時間 ─────────────────────────────────────
    def _compute_target(self) -> tuple[bool, str]:
        if self._mode.get() == "minutes":
            try:
                mins = int(self._min_var.get())
                if mins <= 0:
                    return False, "請輸入大於 0 的分鐘數"
            except ValueError:
                return False, "分鐘數無效"
            self._target_ts = time.time() + mins * 60
        else:
            raw = self._clock_var.get().strip()
            try:
                t = datetime.strptime(raw, "%H:%M")
                now = datetime.now()
                target = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
                if target <= now:
                    target += timedelta(days=1)
                self._target_ts = target.timestamp()
            except ValueError:
                return False, "時刻格式應為 HH:MM"
        return True, ""

    # ── 控制邏輯 ─────────────────────────────────────────
    def _start(self):
        if self._paused:
            # 從暫停恢復：用剩餘秒數重新計算 target
            self._target_ts = time.time() + self._remaining
            self._paused = False
        else:
            ok, err = self._compute_target()
            if not ok:
                messagebox.showerror("輸入錯誤", err)
                return
        self._running = True
        self._stop_evt.clear()
        self._start_btn.configure(state="disabled")
        self._pause_btn.configure(state="normal")
        self._status_label.configure(text="計時中…", text_color=PALETTE["green"])

        self._thread = threading.Thread(target=self._tick, daemon=True)
        self._thread.start()

    def _pause(self):
        if not self._running:
            return
        self._running = False
        self._paused  = True
        self._stop_evt.set()
        self._start_btn.configure(state="normal", text="▶ 繼續")
        self._pause_btn.configure(state="disabled")
        self._status_label.configure(text="已暫停", text_color=PALETTE["orange"])

    def _reset(self):
        self._running   = False
        self._paused    = False
        self._target_ts = None
        self._remaining = 0
        self._stop_evt.set()
        self._start_btn.configure(state="normal", text="▶ 開始")
        self._pause_btn.configure(state="disabled")
        self._countdown_label.configure(text="──:──:──",
                                         text_color=PALETTE["text"])
        self._status_label.configure(text="待機中", text_color=PALETTE["subtext"])

    def _remove(self):
        self._reset()
        self._on_remove(self)

    # ── 計時執行緒 ────────────────────────────────────────
    def _tick(self):
        while not self._stop_evt.is_set():
            remaining = self._target_ts - time.time()
            if remaining <= 0:
                self._remaining = 0
                self.after(0, self._done)
                return
            self._remaining = int(remaining)
            self.after(0, self._update_display, self._remaining)
            self._stop_evt.wait(0.5)

    def _update_display(self, secs: int):
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        self._countdown_label.configure(
            text=f"{h:02d}:{m:02d}:{s:02d}",
            text_color=PALETTE["red"] if secs <= 60 else PALETTE["text"]
        )

    def _done(self):
        self._running = False
        self._countdown_label.configure(text="00:00:00",
                                         text_color=PALETTE["red"])
        self._status_label.configure(text="時間到！", text_color=PALETTE["red"])
        self._start_btn.configure(state="normal", text="▶ 開始")
        self._pause_btn.configure(state="disabled")

        msg = self._msg_entry.get().strip() or "時間到！"
        self._show_notify(msg)

    def _show_notify(self, msg: str):
        win = ctk.CTkToplevel(self)
        win.title("⏰ 提醒")
        win.geometry("360x220")
        win.configure(fg_color=PALETTE["bg"])
        win.lift()
        win.attributes("-topmost", True)

        ctk.CTkLabel(win, text="⏰", font=("Segoe UI Emoji", 48)).pack(pady=(24, 4))
        ctk.CTkLabel(win, text=msg, font=("Consolas", 16, "bold"),
                     text_color=PALETTE["text"],
                     wraplength=300).pack(pady=4)
        ctk.CTkLabel(win, text=f"計時器 #{self._id}",
                     font=("Consolas", 11),
                     text_color=PALETTE["subtext"]).pack()
        ctk.CTkButton(win, text="知道了", font=("Consolas", 13),
                      fg_color=PALETTE["accent"], hover_color="#1f6feb",
                      text_color="#fff", width=120,
                      command=win.destroy).pack(pady=16)


# ── 主視窗 ────────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("番茄計時器")
        self.geometry("520x720")
        self.minsize(460, 500)
        self.configure(fg_color=PALETTE["bg"])
        self._cards: list[TimerCard] = []
        self._build()

    def _build(self):
        # 頂欄
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(18, 8))
        ctk.CTkLabel(header, text="⏱ 番茄計時器",
                     font=("Consolas", 20, "bold"),
                     text_color=PALETTE["accent"]).pack(side="left")
        ctk.CTkButton(header, text="＋ 新增計時器",
                      width=130, height=34, corner_radius=8,
                      font=("Consolas", 12, "bold"),
                      fg_color=PALETTE["accent"], hover_color="#1f6feb",
                      text_color="#fff",
                      command=self._add_card).pack(side="right")

        # 捲動區
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                               scrollbar_button_color=PALETTE["border"])
        self._scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # 預設加一張卡片
        self._add_card()

    def _add_card(self):
        card = TimerCard(self._scroll, on_remove=self._remove_card)
        card.pack(fill="x", pady=8)
        self._cards.append(card)

    def _remove_card(self, card: TimerCard):
        card.pack_forget()
        card.destroy()
        self._cards.remove(card)


if __name__ == "__main__":
    app = App()
    app.mainloop()