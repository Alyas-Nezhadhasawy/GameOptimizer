from ui.generic_tweak_tab import GenericTweakTab
from data.services_tweaks import build
from core import i18n


class ServicesTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Unwanted Services",
                          "غیرفعال‌سازی سرویس‌های اضافی ویندوز" if i18n.LANG == "fa"
                          else "Disable unneeded Windows services",
                          build(), **kwargs)
