"""
GenericTweakTab
----------------
Every tab that's just "a list of toggles" is built from this widget + a
list[Tweak]. Language is resolved once, at construction time, via core.i18n
(chosen on the splash screen before any tab exists) — no live re-render
needed.

Behavior:
  - Switches start disabled/greyed while a BACKGROUND thread calls
    is_applied() for every tweak (registry reads / bcdedit / powercfg calls
    are slow — never run them on the UI thread). Once done, switches that
    are already applied (by this app before, manually by the user, or by
    another tool) light up automatically.
  - Each switch has its own busy-lock: clicking it spawns exactly one
    background worker; a click while it's already running is ignored
    instead of stacking another slow subprocess call on top of it.
  - "Apply Selected" / "Restore Defaults" run through a ProgressDialog with
    a real step-by-step percentage and a final success message.
"""
import threading
import customtkinter as ctk
from core.tweak_base import RISK_SAFE, RISK_MEDIUM, RISK_HIGH
from core import i18n
from core import theme
from ui.progress_dialog import ProgressDialog

RISK_COLORS = {RISK_SAFE: theme.SUCCESS, RISK_MEDIUM: theme.WARNING, RISK_HIGH: theme.DANGER}


class GenericTweakTab(ctk.CTkFrame):
    def __init__(self, master, title: str, subtitle: str, tweaks: list, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.tweaks = tweaks
        self.switches = {}
        self.switch_widgets = {}
        self._busy_ids = set()
        self._bulk_running = False

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 4))
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 20, "bold")).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(header, text=subtitle, text_color=theme.TEXT_MUTED,
                         font=("Segoe UI", 12)).pack(anchor="w")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=(0, 8))
        self.apply_btn = ctk.CTkButton(actions, text=i18n.t("apply_selected"),
                                        command=self.apply_selected, width=180)
        self.apply_btn.pack(side="left", padx=(0, 8))
        self.restore_btn = ctk.CTkButton(actions, text=i18n.t("restore_default"), fg_color=theme.BG_HOVER,
                                          hover_color=theme.BORDER, command=self.restore_all, width=200)
        self.restore_btn.pack(side="left")
        self.scan_status = ctk.CTkLabel(actions, text=i18n.t("scanning"),
                                         text_color=theme.TEXT_MUTED, font=("Segoe UI", 11))
        self.scan_status.pack(side="left", padx=14)

        self._build_extra_top()  # hook for subclasses — runs before self.scroll exists

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=12, pady=4)

        for tweak in self.tweaks:
            self._build_row(tweak)

        threading.Thread(target=self._scan_states, daemon=True).start()

    def _build_extra_top(self):
        """Override in a subclass to insert content between the action buttons and the list."""
        pass

    # ---------- row building ----------

    def _build_row(self, tweak):
        row = ctk.CTkFrame(self.scroll, corner_radius=10)
        row.pack(fill="x", pady=5, padx=6)

        text_col = ctk.CTkFrame(row, fg_color="transparent")
        text_col.pack(side="right", fill="x", expand=True, padx=12, pady=10)

        top = ctk.CTkFrame(text_col, fg_color="transparent")
        top.pack(fill="x", anchor="e")
        ctk.CTkLabel(top, text=i18n.tweak_name(tweak), font=("Segoe UI", 14, "bold")).pack(side="right")
        ctk.CTkLabel(top, text=f"  [{i18n.t('risk_' + tweak.risk)}]",
                     text_color=RISK_COLORS[tweak.risk],
                     font=("Segoe UI", 11, "bold")).pack(side="right")

        ctk.CTkLabel(text_col, text=i18n.tweak_desc(tweak), text_color=theme.TEXT_MUTED,
                     font=("Segoe UI", 11), wraplength=560, justify="right").pack(anchor="e")

        var = ctk.BooleanVar(value=False)
        switch = ctk.CTkSwitch(row, text="", variable=var, state="disabled",
                                command=lambda t=tweak, v=var: self._toggle(t, v))
        switch.pack(side="left", padx=14)
        self.switches[tweak.id] = var
        self.switch_widgets[tweak.id] = switch

    # ---------- background scan on open ----------

    def _scan_states(self):
        results = {}
        for tweak in self.tweaks:
            try:
                results[tweak.id] = bool(tweak.is_applied())
            except Exception:
                results[tweak.id] = False
        self.after(0, lambda: self._apply_scan_results(results))

    def _apply_scan_results(self, results):
        for tid, applied in results.items():
            if tid not in self.switches:
                continue
            self.switches[tid].set(applied)
            self.switch_widgets[tid].configure(state="normal")
        self.scan_status.configure(text=i18n.t("scanned"))

    # ---------- single-switch toggle (threaded + locked) ----------

    def _toggle(self, tweak, var):
        if tweak.id in self._busy_ids:
            var.set(not var.get())  # revert the click visually — an op is already running
            return
        self._busy_ids.add(tweak.id)
        sw = self.switch_widgets[tweak.id]
        sw.configure(state="disabled")
        target_state = var.get()

        def worker():
            error = None
            try:
                if target_state:
                    tweak.apply()
                else:
                    tweak.revert()
            except Exception as e:
                error = e

            def done():
                self._busy_ids.discard(tweak.id)
                sw.configure(state="normal")
                if error is not None:
                    var.set(not target_state)
                    self._error(f"{i18n.tweak_name(tweak)}: {error}")

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    # ---------- bulk actions (threaded, with progress dialog) ----------

    def apply_selected(self):
        self._run_bulk([t for t in self.tweaks if self.switches[t.id].get()], action="apply")

    def restore_all(self):
        self._run_bulk(self.tweaks, action="revert")

    def _run_bulk(self, tweak_list, action):
        if self._bulk_running or not tweak_list:
            return
        self._bulk_running = True
        self.apply_btn.configure(state="disabled")
        self.restore_btn.configure(state="disabled")
        title = i18n.t("apply_selected") if action == "apply" else i18n.t("restore_default")
        dialog = ProgressDialog(self, title=title + "...")
        total = len(tweak_list)

        def worker():
            failed = []
            for i, tweak in enumerate(tweak_list, start=1):
                name = i18n.tweak_name(tweak)
                dialog.update_progress((i - 1) / total, f"{name} ({i}/{total})")
                try:
                    if action == "apply":
                        tweak.apply()
                    else:
                        tweak.revert()
                        self.after(0, lambda t=tweak: self.switches[t.id].set(False))
                except Exception as e:
                    failed.append((name, str(e)))
                dialog.update_progress(i / total, f"{name} ({i}/{total})")

            def wrap_up():
                self._bulk_running = False
                self.apply_btn.configure(state="normal")
                self.restore_btn.configure(state="normal")
                if failed:
                    msg = f"✅ {total - len(failed)}/{total} · ❌ {len(failed)}"
                else:
                    msg = f"✅ {total}/{total}"
                dialog.finish(msg)

            self.after(0, wrap_up)

        threading.Thread(target=worker, daemon=True).start()

    def _error(self, msg):
        dialog = ctk.CTkToplevel(self)
        dialog.title(i18n.t("error_title"))
        dialog.geometry("380x140")
        dialog.attributes("-topmost", True)
        ctk.CTkLabel(dialog, text=msg, wraplength=340, justify="right").pack(pady=20, padx=20)
        ctk.CTkButton(dialog, text=i18n.t("ok"), command=dialog.destroy).pack()
