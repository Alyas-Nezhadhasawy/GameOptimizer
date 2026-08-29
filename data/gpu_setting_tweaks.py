from core.tweak_base import Tweak, RISK_SAFE
from data._helpers import reg_toggle


def build():
    tweaks = []

    a, r, c = reg_toggle("gpu_pref_max_perf",
        r"HKCU\Software\Microsoft\DirectX\UserGpuPreferences",
        "DirectXUserGlobalSettings", "SwapEffectUpgradeEnable=1;", "", rtype="REG_SZ")
    tweaks.append(Tweak("gpu_pref_max_perf", "فعال‌سازی SwapEffect Upgrade",
        "برخی بازی‌های قدیمی‌تر رو مجبور می‌کنه از مدل‌های جدیدتر presentation استفاده کنن (لتنسی کمتر).",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("tdr_level",
        r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
        "TdrLevel", 3, 1)
    tweaks.append(Tweak("tdr_level", "بازگردانی TDR سطح پیش‌فرض (پایداری درایور)",
        "اطمینان از این‌که Timeout Detection & Recovery درایور گرافیک روی حالت استاندارد فعاله.",
        a, r, c, RISK_SAFE))

    return tweaks
