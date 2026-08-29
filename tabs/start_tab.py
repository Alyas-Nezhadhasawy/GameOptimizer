import subprocess
import threading
import customtkinter as ctk

from core import admin_utils, registry_engine as reg, service_engine as svc
from data.debloat_apps import BLOAT_APPS
from ui.progress_dialog import ProgressDialog
from core import i18n
from core import theme


class StartTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        ctk.CTkLabel(self, text=i18n.t("start_title"), font=("Segoe UI", 20, "bold")
                     ).pack(anchor="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(self, text=i18n.t("start_subtitle"),
                     text_color=theme.TEXT_MUTED, font=("Segoe UI", 12)).pack(anchor="w", padx=20)

        # ---- Backup section ----
        backup_box = ctk.CTkFrame(self, corner_radius=12)
        backup_box.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(backup_box, text=i18n.t("backup_section"),
                     font=("Segoe UI", 15, "bold")).pack(anchor="e", padx=16, pady=(12, 4))
        self.backup_status = ctk.CTkLabel(backup_box, text=i18n.t("backup_not_yet"),
                                           text_color=theme.TEXT_MUTED)
        self.backup_status.pack(anchor="e", padx=16)
        ctk.CTkButton(backup_box, text=i18n.t("backup_btn"),
                      command=self.run_backup).pack(anchor="e", padx=16, pady=12)

        # ---- Debloat section ----
        debloat_box = ctk.CTkFrame(self, corner_radius=12)
        debloat_box.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        ctk.CTkLabel(debloat_box, text=i18n.t("debloat_section"),
                     font=("Segoe UI", 15, "bold")).pack(anchor="e", padx=16, pady=(12, 4))

        scroll = ctk.CTkScrollableFrame(debloat_box, fg_color="transparent", height=220)
        scroll.pack(fill="both", expand=True, padx=8)
        self.app_vars = {}
        for pkg, label in BLOAT_APPS:
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(scroll, text=label, variable=var)
            cb.pack(anchor="e", padx=12, pady=3)
            self.app_vars[pkg] = var

        ctk.CTkButton(debloat_box, text=i18n.t("debloat_btn"),
                      command=self.run_debloat).pack(anchor="e", padx=16, pady=12)

        # ---- Windows Update section ----
        update_box = ctk.CTkFrame(self, corner_radius=12)
        update_box.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(update_box, text=i18n.t("update_section"),
                     font=("Segoe UI", 15, "bold")).pack(anchor="e", padx=16, pady=(12, 4))
        self.update_switch = ctk.CTkSwitch(update_box, text=i18n.t("update_checking"),
                                            state="disabled", command=self.toggle_update)
        self.update_switch.pack(anchor="e", padx=16, pady=(0, 12))
        self._update_busy = False
        threading.Thread(target=self._scan_update_state, daemon=True).start()

    def _scan_update_state(self):
        try:
            already_disabled = svc.get_start_type("wuauserv") == "disabled"
        except Exception:
            already_disabled = False

        def apply_result():
            self.update_switch.configure(state="normal", text=i18n.t("update_btn"))
            if already_disabled:
                self.update_switch.select()
            else:
                self.update_switch.deselect()

        self.after(0, apply_result)

    def run_backup(self):
        if getattr(self, "_backup_running", False):
            return
        self._backup_running = True
        self.backup_status.configure(text="در حال ساخت بک‌آپ...")
        dialog = ProgressDialog(self, title="در حال ساخت بک‌آپ سیستم...")

        def worker():
            try:
                dialog.update_progress(0.1, "فعال‌سازی System Protection...")
                admin_utils.enable_system_protection()

                dialog.update_progress(0.3, "ساخت System Restore Point... (ممکنه چند دقیقه طول بکشه)")
                admin_utils.create_restore_point("GamingOptimizer - Before Tweaks")

                dialog.update_progress(0.75, "Export گرفتن از رجیستری HKLM/HKCU...")
                reg.export_full_registry_backup(r"C:\GamingOptimizerBackups")

                dialog.update_progress(1.0, "تمام شد.")
                dialog.finish("✅ بک‌آپ و Restore Point با موفقیت ساخته شد.")
                self.after(0, lambda: self.backup_status.configure(
                    text="✅ آخرین بک‌آپ با موفقیت ساخته شد."))
            except Exception as e:
                dialog.fail(f"خطا در ساخت بک‌آپ: {e}")
                self.after(0, lambda: self.backup_status.configure(text=f"❌ خطا: {e}"))
            finally:
                self._backup_running = False

        threading.Thread(target=worker, daemon=True).start()

    def run_debloat(self):
        selected = [(pkg, label) for pkg, label in BLOAT_APPS if self.app_vars[pkg].get()]
        if not selected:
            return
        dialog = ProgressDialog(self, title="در حال حذف برنامه‌ها...")
        total = len(selected)

        def worker():
            for i, (pkg, label) in enumerate(selected, start=1):
                dialog.update_progress((i - 1) / total, f"در حال حذف {label}...")
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                     f"Get-AppxPackage -Name '{pkg}' -AllUsers | Remove-AppxPackage"],
                    capture_output=True)
                dialog.update_progress(i / total, f"{label} حذف شد ({i}/{total})")
            dialog.finish(f"✅ {total} برنامه با موفقیت حذف شد.")

        threading.Thread(target=worker, daemon=True).start()

    def toggle_update(self):
        if self._update_busy:
            # cancel the click visually — a previous op is still running
            (self.update_switch.deselect() if self.update_switch.get()
             else self.update_switch.select())
            return
        self._update_busy = True
        target_on = self.update_switch.get()
        self.update_switch.configure(state="disabled", text="در حال اعمال...")
        tid = "wu_disable"

        def worker():
            try:
                if target_on:
                    svc.set_start_type("wuauserv", "disabled", tid)
                    reg.write_value(
                        r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
                        "NoAutoUpdate", 1, "REG_DWORD", tid)
                else:
                    svc.restore_service("wuauserv")
                    reg.restore_tweak(tid)
                error = None
            except Exception as e:
                error = e

            def done():
                self._update_busy = False
                self.update_switch.configure(state="normal", text=i18n.t("update_btn"))
                if error is not None:
                    (self.update_switch.deselect() if target_on
                     else self.update_switch.select())

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()
