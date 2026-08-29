import os
import customtkinter as ctk
from PIL import Image
from core import i18n
from core import theme

ICON_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "icons")
APP_VERSION = "1.0.0"

# order matches the spec exactly
SECTIONS = [
    ("start", "Start", "start"),
    ("registry", "Registry & BCD Tweaks", "registry"),
    ("windows_settings", "Windows Settings", "windows_settings"),
    ("control_panel", "Control Panel", "control_panel"),
    ("power_plan", "Power Plan", "power"),
    ("gpu_setting", "GPU Setting", "gpu"),
    ("gpu_vendor", "GPU Vendor Guide" if i18n.LANG == "en" else "راهنمای کارت گرافیک", "gpu_tweaks"),
    ("games", "Game Presets" if i18n.LANG == "en" else "تنظیمات بازی‌ها", "priority"),
    ("cleanup", "Clean Up", "cleanup"),
    ("services", "Unwanted Services", "services"),
    ("msi_mode", "MSI Mode Tools", "msi"),
    ("gpu_tweaks", "GPU Tweaks", "gpu_tweaks"),
    ("network", "Network Tweak", "network"),
    ("ram", "Ram Process", "ram"),
    ("adobe", "Adobe High Performance", "adobe"),
    ("priority", "Game High Priority", "priority"),
    ("startup", "Startup / Autorun Apps", "startup"),
]


class Sidebar(ctk.CTkScrollableFrame):
    def __init__(self, master, on_select, **kwargs):
        super().__init__(master, width=230, fg_color=theme.BG_SIDEBAR, corner_radius=0, **kwargs)
        self.on_select = on_select
        self.buttons = {}
        self._icons = {}

        # Logo + title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=(10, 14), padx=10, fill="x")

        logo_img = Image.open(os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png"))
        logo_ctk = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(32, 32))
        ctk.CTkLabel(title_frame, text="", image=logo_ctk).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(title_frame, text="Gaming Optimizer", font=("Segoe UI", 17, "bold"),
                     text_color=theme.RED).pack(side="left")

        for key, label, icon_name in SECTIONS:
            img = self._load_icon(icon_name)
            btn = ctk.CTkButton(
                self, text=label, image=img, anchor="w",
                fg_color="transparent", hover_color=theme.BG_HOVER,
                text_color=theme.TEXT_PRIMARY,
                font=("Segoe UI", 13), height=38, corner_radius=6,
                command=lambda k=key: self._select(k),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.buttons[key] = btn

        ctk.CTkLabel(self, text=f"v{APP_VERSION}", text_color=theme.TEXT_MUTED,
                     font=("Segoe UI", 10)).pack(pady=(10, 8))

    def _load_icon(self, name):
        if name not in self._icons:
            path = os.path.join(ICON_DIR, f"{name}.png")
            if os.path.exists(path):
                pil = Image.open(path)
                self._icons[name] = ctk.CTkImage(light_image=pil, dark_image=pil, size=(20, 20))
            else:
                self._icons[name] = None
        return self._icons[name]

    def _select(self, key):
        for k, b in self.buttons.items():
            b.configure(fg_color=theme.RED if k == key else "transparent",
                        text_color=theme.TEXT_ON_RED if k == key else theme.TEXT_PRIMARY)
        self.on_select(key)
