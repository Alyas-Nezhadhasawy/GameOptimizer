import subprocess
import threading
import customtkinter as ctk
from ui.generic_tweak_tab import GenericTweakTab
from data.gpu_setting_tweaks import build as build_tweaks
from core import i18n
from core import theme


def detect_gpu() -> str:
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"],
            capture_output=True, text=True)
        names = [l.strip() for l in out.stdout.splitlines() if l.strip()]
        return " / ".join(names) if names else "?"
    except Exception:
        return "?"


class GPUSettingTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, i18n.t("gpu_setting_title"), i18n.t("gpu_setting_subtitle"),
                          build_tweaks(), **kwargs)

    def _build_extra_top(self):
        # called by GenericTweakTab.__init__ BEFORE self.scroll is created,
        # so there's no ordering issue like the old before=self.scroll approach.
        info = ctk.CTkFrame(self, corner_radius=10, fg_color=theme.BG_CARD)
        info.pack(fill="x", padx=20, pady=(0, 8))
        self._gpu_label = ctk.CTkLabel(info, text=i18n.t("gpu_detecting"),
                                        text_color=theme.RED, font=("Segoe UI", 12, "bold"))
        self._gpu_label.pack(padx=14, pady=10, anchor="e")
        threading.Thread(target=self._detect_gpu_async, daemon=True).start()

    def _detect_gpu_async(self):
        name = detect_gpu()
        self.after(0, lambda: self._gpu_label.configure(text=f"{i18n.t('gpu_detected')} {name}"))
