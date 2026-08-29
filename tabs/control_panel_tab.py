from ui.generic_tweak_tab import GenericTweakTab
from data.control_panel_tweaks import build
from core import i18n


class ControlPanelTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Control Panel",
                          "تنظیمات ویژه‌ی صدا، موس و گرافیک ویندوز" if i18n.LANG == "fa"
                          else "Special sound, mouse and graphics settings",
                          build(), **kwargs)
