from ui.generic_tweak_tab import GenericTweakTab
from data.gpu_tweaks import build
from core import i18n


class GPUTweaksTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "GPU Tweaks",
                          "بهترین پروفایل درایور برای عملکرد و دمای بهینه" if i18n.LANG == "fa"
                          else "Best driver profile for performance and temps",
                          build(), **kwargs)
