import threading
import customtkinter as ctk
from core import startup_engine as se
from core import i18n
from core import theme

SOURCE_LABELS = {
    "run_key": "Registry Run Key",
    "startup_folder": "Startup Folder" if i18n.LANG == "en" else "پوشه‌ی Startup",
    "scheduled_task": "Scheduled Task",
}


class StartupAppsTab(ctk.CTkFrame):
    """
    این تب همه‌ی برنامه‌هایی که به‌صورت پنهان با ویندوز اجرا می‌شن رو
    (چه از Registry Run key، چه از پوشه‌ی Startup، چه از Task Scheduler)
    پیدا می‌کنه و با یک سوییچ ساده قابل خاموش/روشن کردنه — هیچی حذف نمی‌شه،
    فقط غیرفعال می‌شه و هر وقت خواستی برمی‌گرده.

    اسکن (که چند subprocess/PowerShell کند صدا می‌زنه) همیشه توی یک ترد
    پس‌زمینه اجرا می‌شه تا UI هنگ نکنه؛ هر سوییچ هم قفل جدا داره تا کلیک‌های
    پشت‌سرهم روی چند مورد باعث تداخل/کرش نشه.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._busy_keys = set()
        self._scanning = False

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 4))
        ctk.CTkLabel(header, text=i18n.t("startup_title"),
                     font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(header,
                     text=i18n.t("startup_subtitle"),
                     text_color=theme.TEXT_MUTED, font=("Segoe UI", 12)).pack(anchor="w")

        self.refresh_btn = ctk.CTkButton(self, text=i18n.t("rescan"), command=self.refresh)
        self.refresh_btn.pack(anchor="w", padx=20, pady=8)
        self.status_label = ctk.CTkLabel(self, text="", text_color=theme.TEXT_MUTED)
        self.status_label.pack(anchor="w", padx=20)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=12, pady=4)

        self.refresh()

    def refresh(self):
        if self._scanning:
            return
        self._scanning = True
        self.refresh_btn.configure(state="disabled")
        self.status_label.configure(text=i18n.t("startup_scanning"))
        for w in self.scroll.winfo_children():
            w.destroy()

        def worker():
            try:
                apps = se.list_all()
                error = None
            except Exception as e:
                apps = []
                error = str(e)
            self.after(0, lambda: self._on_scanned(apps, error))

        threading.Thread(target=worker, daemon=True).start()

    def _on_scanned(self, apps, error):
        self._scanning = False
        self.refresh_btn.configure(state="normal")
        if error:
            self.status_label.configure(text=f"خطا در اسکن: {error}")
            return
        if not apps:
            self.status_label.configure(text=i18n.t("startup_none"))
            return
        self.status_label.configure(
            text=f"✅ {len(apps)} برنامه پیدا شد — وضعیت فعلی هرکدوم (روشن/خاموش) به‌صورت خودکار نشون داده شده.")
        for app in apps:
            self._row(app)

    def _row_key(self, app):
        if app["source"] == "run_key":
            return ("run_key", app["path"], app["name"])
        if app["source"] == "startup_folder":
            return ("startup_folder", app["folder"], app["name"])
        return ("scheduled_task", app["path"], app["name"])

    def _row(self, app):
        row = ctk.CTkFrame(self.scroll, corner_radius=10)
        row.pack(fill="x", pady=5, padx=6)

        text_col = ctk.CTkFrame(row, fg_color="transparent")
        text_col.pack(side="right", fill="x", expand=True, padx=12, pady=10)
        ctk.CTkLabel(text_col, text=app["name"], font=("Segoe UI", 13, "bold")
                     ).pack(anchor="e")
        ctk.CTkLabel(text_col, text=SOURCE_LABELS[app["source"]],
                     text_color=theme.TEXT_MUTED, font=("Segoe UI", 10)).pack(anchor="e")

        var = ctk.BooleanVar(value=app["enabled"])
        switch = ctk.CTkSwitch(row, text="فعال" if app["enabled"] else "غیرفعال",
                                variable=var,
                                command=lambda a=app, v=var, s=None: self._toggle(a, v))
        switch.pack(side="left", padx=14)

    def _toggle(self, app, var):
        key = self._row_key(app)
        if key in self._busy_keys:
            var.set(not var.get())
            return
        self._busy_keys.add(key)
        enable = var.get()

        def worker():
            error = None
            try:
                if app["source"] == "run_key":
                    se.toggle_run_key_app(app["hive"], app["path"], app["name"], enable)
                elif app["source"] == "startup_folder":
                    se.toggle_startup_folder_app(app["folder"], app["name"], enable)
                elif app["source"] == "scheduled_task":
                    se.toggle_scheduled_task(app["path"], app["name"], enable)
            except Exception as e:
                error = e

            def done():
                self._busy_keys.discard(key)
                if error is not None:
                    var.set(not enable)
                    self.status_label.configure(text=f"خطا: {error}")
                else:
                    self.refresh()  # re-render so the row's label/state reflect reality exactly
            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()
