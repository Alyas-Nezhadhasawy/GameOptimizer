from ui.generic_tweak_tab import GenericTweakTab
from data.windows_settings_tweaks import build
from core import i18n


class WindowsSettingsTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Windows Settings",
                          "بهینه‌سازی تنظیمات ویندوز برای بهترین پرفورمنس" if i18n.LANG == "fa"
                          else "Optimize Windows settings for best performance",
                          build(), **kwargs)
