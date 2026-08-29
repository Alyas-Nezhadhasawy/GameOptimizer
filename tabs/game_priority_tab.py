import os
import winreg
import customtkinter as ctk
from tkinter import filedialog
from core import i18n
from core import theme

BASE_PATH = r"Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{exe}\PerfOptions"


class GamePriorityTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text=i18n.t("priority_title"), font=("Segoe UI", 20, "bold")
                     ).pack(anchor="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(self,
                     text=i18n.t("priority_subtitle"),
                     text_color=theme.TEXT_MUTED, font=("Segoe UI", 12), wraplength=600, justify="right"
                     ).pack(anchor="w", padx=20)

        box = ctk.CTkFrame(self, corner_radius=12)
        box.pack(fill="x", padx=20, pady=16)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(16, 6))
        self.exe_entry = ctk.CTkEntry(row, placeholder_text=i18n.t("priority_placeholder"))
        self.exe_entry.pack(side="right", fill="x", expand=True, padx=(8, 0))
        ctk.CTkButton(row, text=i18n.t("priority_browse"), width=140,
                      command=self.browse_exe).pack(side="right")

        self.priority_var = ctk.StringVar(value="High")
        ctk.CTkSegmentedButton(box, values=["AboveNormal", "High", "Realtime"],
                               variable=self.priority_var).pack(padx=16, pady=6)

        btn_row = ctk.CTkFrame(box, fg_color="transparent")
        btn_row.pack(padx=16, pady=(6, 16), anchor="e")
        ctk.CTkButton(btn_row, text=i18n.t("priority_apply"),
                      command=self.apply_now).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_row, text=i18n.t("priority_export"), fg_color="#555",
                      hover_color="#444", command=self.export_reg).pack(side="right")

        self.status = ctk.CTkLabel(self, text="", text_color=theme.TEXT_MUTED)
        self.status.pack(anchor="w", padx=20)

        ctk.CTkLabel(self, text=i18n.t("priority_configured"), font=("Segoe UI", 13, "bold")
                     ).pack(anchor="e", padx=20, pady=(10, 0))
        self.list_box = ctk.CTkTextbox(self, height=120)
        self.list_box.pack(fill="x", padx=20, pady=(4, 20))
        self.refresh_list()

    def browse_exe(self):
        path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if path:
            self.exe_entry.delete(0, "end")
            self.exe_entry.insert(0, os.path.basename(path))

    def _target_exe(self):
        name = self.exe_entry.get().strip()
        if not name:
            return None
        return name if name.lower().endswith(".exe") else name + ".exe"

    def apply_now(self):
        exe = self._target_exe()
        if not exe:
            self.status.configure(text="اول اسم فایل exe بازی رو وارد کن.")
            return
        path = BASE_PATH.format(exe=exe)
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        winreg.SetValueEx(key, "CpuPriorityClass", 0, winreg.REG_DWORD,
                           self._priority_value())
        winreg.CloseKey(key)
        self.status.configure(text=f"✅ اولویت {exe} روی {self.priority_var.get()} تنظیم شد.")
        self.refresh_list()

    def _priority_value(self):
        return {"AboveNormal": 5, "High": 3, "Realtime": 4}[self.priority_var.get()]

    def export_reg(self):
        exe = self._target_exe()
        if not exe:
            self.status.configure(text="اول اسم فایل exe بازی رو وارد کن.")
            return
        val = self._priority_value()
        reg_path = f"HKEY_LOCAL_MACHINE\\{BASE_PATH.format(exe=exe)}"
        content = (
            "Windows Registry Editor Version 5.00\r\n\r\n"
            f"[{reg_path}]\r\n"
            f'"CpuPriorityClass"=dword:{val:08x}\r\n'
        )
        save_path = filedialog.asksaveasfilename(
            defaultextension=".reg",
            initialfile="GameHighPriority.reg",
            filetypes=[("Registry file", "*.reg")])
        if save_path:
            with open(save_path, "w", encoding="utf-16") as f:
                f.write(content)
            self.status.configure(text=f"✅ فایل .reg ساخته شد: {save_path}")

    def refresh_list(self):
        self.list_box.delete("1.0", "end")
        base = r"Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base) as key:
                i = 0
                lines = []
                while True:
                    try:
                        sub = winreg.EnumKey(key, i)
                        i += 1
                        try:
                            with winreg.OpenKey(key, sub + "\\PerfOptions") as pk:
                                v, _ = winreg.QueryValueEx(pk, "CpuPriorityClass")
                                lines.append(f"{sub}  →  priority={v}")
                        except FileNotFoundError:
                            continue
                    except OSError:
                        break
                self.list_box.insert("1.0", "\n".join(lines) or "هیچ بازی‌ای هنوز تنظیم نشده.")
        except Exception:
            self.list_box.insert("1.0", "—")
