from core.tweak_base import Tweak, RISK_SAFE, RISK_MEDIUM
from data._helpers import reg_toggle


def build():
    tweaks = []

    a, r, c = reg_toggle("hags_on",
        r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\GraphicsDrivers",
        "HwSchMode", 2, 1)
    tweaks.append(Tweak("hags_on", "فعال‌سازی Hardware-Accelerated GPU Scheduling",
        "زمان‌بندی صف GPU رو از درایور به خود کارت گرافیک منتقل می‌کنه؛ روی برخی سیستم‌ها لتنسی رو کم می‌کنه.",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("tdr_delay",
        r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
        "TdrDelay", 8, 2)
    tweaks.append(Tweak("tdr_delay", "افزایش TDR Delay",
        "مانع از ری‌استارت درایور گرافیک هنگام رندرهای سنگین/آورکلاک می‌شه (کرش کمتر، نه افزایش سرعت).",
        a, r, c, RISK_MEDIUM))

    a, r, c = reg_toggle("fso_off",
        r"HKCU\System\GameConfigStore",
        "GameDVR_FSEBehaviorMode", 2, 0)
    tweaks.append(Tweak("fso_off", "غیرفعال‌سازی Fullscreen Optimizations (سراسری)",
        "بعضی بازی‌ها با Exclusive Fullscreen واقعی لگ کمتری نسبت به حالت بهینه‌شده‌ی ویندوز دارن.",
        a, r, c, RISK_SAFE))

    return tweaks
