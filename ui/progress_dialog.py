import customtkinter as ctk
from core import theme


class ProgressDialog(ctk.CTkToplevel):
    """Modal progress popup — call update_progress()/finish() from any thread (they hop to the UI thread internally)."""

    def __init__(self, master, title="در حال انجام..."):
        super().__init__(master)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set()

        self.status_label = ctk.CTkLabel(self, text="در حال آماده‌سازی...", font=("Segoe UI", 12))
        self.status_label.pack(pady=(22, 10), padx=20)

        self.bar = ctk.CTkProgressBar(self, width=340)
        self.bar.set(0)
        self.bar.pack(pady=4, padx=20)

        self.percent_label = ctk.CTkLabel(self, text="0%", text_color=theme.TEXT_MUTED)
        self.percent_label.pack(pady=(4, 0))

        self._ok_btn = None

    def update_progress(self, fraction: float, text: str = None):
        self.after(0, self._update, fraction, text)

    def _update(self, fraction, text):
        try:
            self.bar.set(fraction)
            self.percent_label.configure(text=f"{int(fraction * 100)}%")
            if text:
                self.status_label.configure(text=text)
        except Exception:
            pass  # dialog may already be closed

    def finish(self, success_text="✅ با موفقیت انجام شد."):
        self.after(0, self._finish, success_text)

    def _finish(self, text):
        try:
            self.bar.set(1)
            self.percent_label.configure(text="100%")
            self.status_label.configure(text=text)
            if not self._ok_btn:
                self._ok_btn = ctk.CTkButton(self, text="باشه", command=self.destroy)
                self._ok_btn.pack(pady=(12, 4))
        except Exception:
            pass

    def fail(self, error_text: str):
        self.after(0, self._finish, f"❌ {error_text}")
