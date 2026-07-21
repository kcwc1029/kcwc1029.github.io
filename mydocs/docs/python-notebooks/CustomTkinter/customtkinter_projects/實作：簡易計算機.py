import customtkinter as ctk

# ── 主題設定 ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("計算機")
        self.geometry("380x600")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a2e")

        # 計算狀態
        self._expression = ""   # 完整算式
        self._current    = "0"  # 顯示中的數字
        self._new_num    = True # 下一次輸入是否為新數字

        self._build_ui()

    # ── 介面建構 ─────────────────────────────────────────
    def _build_ui(self):
        # 顯示區
        display_frame = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=16)
        display_frame.pack(fill="x", padx=20, pady=(24, 12))

        self._expr_label = ctk.CTkLabel(
            display_frame, text="", font=("Consolas", 14),
            text_color="#8892b0", anchor="e"
        )
        self._expr_label.pack(fill="x", padx=16, pady=(12, 0))

        self._main_label = ctk.CTkLabel(
            display_frame, text="0", font=("Consolas", 48, "bold"),
            text_color="#e2e8f0", anchor="e"
        )
        self._main_label.pack(fill="x", padx=16, pady=(0, 16))

        # 按鈕區
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 按鈕佈局：(文字, 欄位跨度, 顏色類型)
        layout = [
            [("AC", 1, "clear"), ("±", 1, "func"), ("%", 1, "func"), ("÷", 1, "op")],
            [("7",  1, "num"),   ("8", 1, "num"),  ("9", 1, "num"),  ("×", 1, "op")],
            [("6",  1, "num"),   ("5", 1, "num"),  ("4", 1, "num"),  ("−", 1, "op")],
            [("1",  1, "num"),   ("2", 1, "num"),  ("3", 1, "num"),  ("+", 1, "op")],
            [("0",  2, "num"),   (".", 1, "num"),   ("=", 1, "eq")],
        ]

        colors = {
            "num":   ("#2d3561", "#e2e8f0"),   # (bg, fg)
            "op":    ("#e94560", "#ffffff"),
            "func":  ("#2d3561", "#cdd6f4"),
            "clear": ("#e94560", "#ffffff"),
            "eq":    ("#00b4d8", "#ffffff"),
        }
        hover = {
            "num":   "#3d4571",
            "op":    "#ff6b6b",
            "func":  "#3d4571",
            "clear": "#ff6b6b",
            "eq":    "#48cae4",
        }

        for row_idx, row in enumerate(layout):
            btn_frame.grid_rowconfigure(row_idx, weight=1, uniform="row")
            col = 0
            for (text, span, kind) in row:
                btn_frame.grid_columnconfigure(col, weight=1, uniform="col")
                bg, fg = colors[kind]
                btn = ctk.CTkButton(
                    btn_frame,
                    text=text,
                    font=("Consolas", 22, "bold"),
                    fg_color=bg,
                    text_color=fg,
                    hover_color=hover[kind],
                    corner_radius=14,
                    command=lambda t=text: self._on_click(t),
                )
                btn.grid(
                    row=row_idx, column=col,
                    columnspan=span, sticky="nsew",
                    padx=5, pady=5
                )
                col += span

    # ── 事件處理 ─────────────────────────────────────────
    def _on_click(self, key: str):
        if key == "AC":
            self._clear()
        elif key == "±":
            self._toggle_sign()
        elif key == "%":
            self._percent()
        elif key in ("÷", "×", "−", "+"):
            self._set_operator(key)
        elif key == "=":
            self._calculate()
        elif key == ".":
            self._add_decimal()
        else:
            self._append_digit(key)

    def _clear(self):
        self._expression = ""
        self._current    = "0"
        self._new_num    = True
        self._refresh()

    def _toggle_sign(self):
        if self._current != "0":
            if self._current.startswith("-"):
                self._current = self._current[1:]
            else:
                self._current = "-" + self._current
            self._refresh()

    def _percent(self):
        try:
            self._current = self._fmt(float(self._current) / 100)
            self._refresh()
        except Exception:
            pass

    def _append_digit(self, d: str):
        if self._new_num:
            self._current = d
            self._new_num = False
        else:
            if self._current == "0":
                self._current = d
            else:
                if len(self._current.replace("-", "").replace(".", "")) < 12:
                    self._current += d
        self._refresh()

    def _add_decimal(self):
        if self._new_num:
            self._current = "0."
            self._new_num = False
        elif "." not in self._current:
            self._current += "."
        self._refresh()

    def _set_operator(self, op: str):
        self._expression = f"{self._current} {op} "
        self._new_num    = True
        self._refresh()

    def _calculate(self):
        if not self._expression:
            return
        try:
            expr = self._expression + self._current
            # 替換為 Python 可計算的符號
            safe = (expr
                    .replace("÷", "/")
                    .replace("×", "*")
                    .replace("−", "-"))
            result = eval(safe)            # noqa: S307
            self._expr_label.configure(text=expr + " =")
            self._current    = self._fmt(result)
            self._expression = ""
            self._new_num    = True
            self._main_label.configure(text=self._current)
            return
        except ZeroDivisionError:
            self._current = "除以零"
        except Exception:
            self._current = "錯誤"
        self._expression = ""
        self._new_num    = True
        self._refresh()

    def _fmt(self, v) -> str:
        """將數值格式化成簡潔字串。"""
        if isinstance(v, float) and v.is_integer():
            return str(int(v))
        s = f"{v:.10g}"
        return s

    def _refresh(self):
        self._expr_label.configure(text=self._expression)
        self._main_label.configure(text=self._current)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()