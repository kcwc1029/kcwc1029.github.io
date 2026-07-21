import customtkinter as ctk
from tkinter import filedialog
import os
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}


class BatchRenameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("批量圖片改名工具")
        self.geometry("700x580")
        self.resizable(False, False)
        self.folder_path = ""
        self.image_files = []
        self._build_ui()

    def _build_ui(self):
        # --- 資料夾選擇區 ---
        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(folder_frame, text="資料夾：",
                     font=("微軟正黑體", 14)).pack(side="left", padx=10)

        self.folder_label = ctk.CTkLabel(folder_frame, text="尚未選擇資料夾",
                                         text_color="gray",
                                         font=("微軟正黑體", 13),
                                         anchor="w")
        self.folder_label.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkButton(folder_frame, text="選擇資料夾", width=120,
                      command=self._select_folder).pack(side="right", padx=10, pady=10)

        # --- 前綴輸入區 ---
        prefix_frame = ctk.CTkFrame(self)
        prefix_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(prefix_frame, text="前綴文字：",
                     font=("微軟正黑體", 14)).pack(side="left", padx=10)

        self.prefix_entry = ctk.CTkEntry(prefix_frame,
                                         placeholder_text="例如：側視圖片",
                                         height=35,
                                         font=("微軟正黑體", 13))
        self.prefix_entry.pack(side="left", fill="x", expand=True, padx=5, pady=10)

        ctk.CTkButton(prefix_frame, text="預覽", width=80,
                      command=self._preview).pack(side="right", padx=10)

        # --- 格式說明 ---
        today = datetime.today().strftime("%Y.%m.%d")
        hint = f"命名格式：前綴文字_{today}_01.jpg"
        ctk.CTkLabel(self, text=hint,
                     text_color="gray",
                     font=("微軟正黑體", 12)).pack(anchor="w", padx=22, pady=(0, 5))

        # --- 預覽區 ---
        ctk.CTkLabel(self, text="更名預覽",
                     font=("微軟正黑體", 14)).pack(anchor="w", padx=22, pady=(5, 2))

        self.preview_box = ctk.CTkTextbox(self, height=300,
                                          font=("Consolas", 12),
                                          state="disabled")
        self.preview_box.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # --- 底部執行區 ---
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.status_label = ctk.CTkLabel(bottom_frame, text="",
                                         font=("微軟正黑體", 13))
        self.status_label.pack(side="left")

        self.execute_btn = ctk.CTkButton(bottom_frame,
                                         text="執行改名",
                                         width=120,
                                         fg_color="#2ECC71",
                                         hover_color="#27AE60",
                                         font=("微軟正黑體", 14, "bold"),
                                         state="disabled",
                                         command=self._execute_rename)
        self.execute_btn.pack(side="right")

        # 初始預覽提示
        self._write_preview("（選擇資料夾並輸入前綴後，點擊「預覽」查看改名結果）")

    # ── 內部方法 ──────────────────────────────────────────

    def _select_folder(self):
        path = filedialog.askdirectory(title="選擇圖片資料夾")
        if not path:
            return
        self.folder_path = path
        self.folder_label.configure(text=path, text_color="white")
        self._scan_folder()

    def _scan_folder(self):
        all_files = sorted(os.listdir(self.folder_path))
        self.image_files = [
            f for f in all_files
            if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
        ]
        count = len(self.image_files)
        if count == 0:
            self._set_status("此資料夾內沒有圖片", "#E74C3C")
        else:
            self._set_status(f"找到 {count} 張圖片，請輸入前綴後點擊「預覽」", "gray")
        self.execute_btn.configure(state="disabled")
        self._write_preview("（請輸入前綴後點擊「預覽」）")

    def _build_new_names(self):
        """回傳 (pairs, error_msg)。pairs 為 [(舊名, 新名), ...]"""
        prefix = self.prefix_entry.get().strip()
        if not prefix:
            return None, "請輸入前綴文字"
        date_str = datetime.today().strftime("%Y.%m.%d")
        pairs = []
        for i, filename in enumerate(self.image_files, start=1):
            ext = os.path.splitext(filename)[1].lower()
            new_name = f"{prefix}_{date_str}_{i:02d}{ext}"
            pairs.append((filename, new_name))
        return pairs, None

    def _preview(self):
        if not self.folder_path:
            self._set_status("請先選擇資料夾", "#E74C3C")
            return
        if not self.image_files:
            self._set_status("資料夾內沒有圖片", "#E74C3C")
            return

        pairs, error = self._build_new_names()
        if error:
            self._set_status(error, "#E74C3C")
            return

        lines = [f"{old}\n    → {new}\n" for old, new in pairs]
        self._write_preview("".join(lines))
        self.execute_btn.configure(state="normal")
        self._set_status(f"共 {len(pairs)} 張圖片待改名，確認無誤後點擊「執行改名」", "gray")

    def _execute_rename(self):
        pairs, error = self._build_new_names()
        if error:
            self._set_status(error, "#E74C3C")
            return

        success, fail = 0, 0
        for old, new in pairs:
            try:
                os.rename(
                    os.path.join(self.folder_path, old),
                    os.path.join(self.folder_path, new)
                )
                success += 1
            except Exception:
                fail += 1

        if fail == 0:
            self._set_status(f"完成！成功改名 {success} 張圖片", "#2ECC71")
            self.execute_btn.configure(state="disabled")
            self._scan_folder()
        else:
            self._set_status(f"完成 {success} 張，失敗 {fail} 張（請確認檔案未被佔用）", "#E67E22")

    # ── 工具方法 ──────────────────────────────────────────

    def _write_preview(self, text: str):
        self.preview_box.configure(state="normal")
        self.preview_box.delete("0.0", "end")
        self.preview_box.insert("0.0", text)
        self.preview_box.configure(state="disabled")

    def _set_status(self, msg: str, color: str):
        self.status_label.configure(text=msg, text_color=color)


if __name__ == "__main__":
    app = BatchRenameApp()
    app.mainloop()
