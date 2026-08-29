import os
import shutil
import threading
import customtkinter as ctk
from core import i18n
from core import theme

TARGETS = [
    ("temp_user", "پوشه‌ی Temp کاربر", lambda: os.environ.get("TEMP", "")),
    ("temp_windows", "پوشه‌ی Temp ویندوز", lambda: r"C:\Windows\Temp"),
    ("prefetch", "Prefetch", lambda: r"C:\Windows\Prefetch"),
]


class CleanUpTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text=i18n.t("cleanup_title"), font=("Segoe UI", 20, "bold")
                     ).pack(anchor="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(self, text=i18n.t("cleanup_subtitle"),
                     text_color=theme.TEXT_MUTED, font=("Segoe UI", 12)).pack(anchor="w", padx=20)

        self.vars = {}
        box = ctk.CTkFrame(self, corner_radius=12)
        box.pack(fill="x", padx=20, pady=16)
        for key, label, _ in TARGETS:
            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(box, text=label, variable=var).pack(anchor="e", padx=16, pady=6)
            self.vars[key] = var

        self.status = ctk.CTkLabel(self, text="", text_color=theme.TEXT_MUTED)
        self.status.pack(anchor="w", padx=20)

        ctk.CTkButton(self, text=i18n.t("cleanup_btn"),
                      command=self.clean).pack(padx=20, pady=8, anchor="w")
        ctk.CTkButton(self, text=i18n.t("cleanup_disk_btn"), fg_color="#555",
                      hover_color="#444", command=self.run_disk_cleanup
                      ).pack(padx=20, pady=(0, 20), anchor="w")

    def clean(self):
        self.status.configure(text="در حال پاکسازی...")

        def worker():
            freed = 0
            for key, label, path_fn in TARGETS:
                if not self.vars[key].get():
                    continue
                path = path_fn()
                freed += self._clear_folder(path)
            mb = freed / (1024 * 1024)
            self.status.configure(text=f"✅ حدود {mb:.1f} مگابایت آزاد شد.")

        threading.Thread(target=worker, daemon=True).start()

    @staticmethod
    def _clear_folder(path):
        freed = 0
        if not path or not os.path.isdir(path):
            return 0
        for entry in os.scandir(path):
            try:
                size = entry.stat().st_size if entry.is_file() else 0
                if entry.is_dir():
                    shutil.rmtree(entry.path, ignore_errors=True)
                else:
                    os.remove(entry.path)
                freed += size
            except (PermissionError, OSError):
                continue  # file in use — skip, don't crash
        return freed

    def run_disk_cleanup(self):
        import subprocess
        subprocess.Popen(["cleanmgr", "/sagerun:1"])
