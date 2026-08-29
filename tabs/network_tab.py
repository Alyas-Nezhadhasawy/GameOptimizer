from ui.generic_tweak_tab import GenericTweakTab
from data.network_tweaks import build
from core import i18n


class NetworkTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Network Tweak",
                          "کاهش پینگ و لگ اتصال اینترنت" if i18n.LANG == "fa"
                          else "Lower ping and connection lag",
                          build(), **kwargs)
