from ui.generic_tweak_tab import GenericTweakTab
from data.registry_bcd_tweaks import build
from core import i18n


class RegistryBCDTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Registry & BCD Tweaks",
                          "FPS بیشتر، لگ و دیلی کمتر" if i18n.LANG == "fa" else "Higher FPS, less lag and delay",
                          build(), **kwargs)
