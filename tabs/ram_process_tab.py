from ui.generic_tweak_tab import GenericTweakTab
from data.ram_tweaks import build
from core import i18n


class RamProcessTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Ram Process",
                          "تنظیمات مخصوص رم برای عملکرد بهینه‌تر" if i18n.LANG == "fa"
                          else "RAM tuning for better performance",
                          build(), **kwargs)
