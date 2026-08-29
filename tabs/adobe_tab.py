from ui.generic_tweak_tab import GenericTweakTab
from data.adobe_tweaks import build
from core import i18n


class AdobeTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Adobe High Performance",
                          "افزایش سرعت نرم‌افزارهای ادوبی" if i18n.LANG == "fa"
                          else "Speed up Adobe Creative Cloud apps",
                          build(), **kwargs)
