from core.tweak_base import Tweak, RISK_SAFE
from data._helpers import reg_toggle


def build():
    tweaks = []

    a, r, c = reg_toggle("mouse_accel_off",
        r"HKCU\Control Panel\Mouse", "MouseSpeed", "0", "1", rtype="REG_SZ")
    tweaks.append(Tweak("mouse_accel_off", "غیرفعال‌سازی Mouse Acceleration",
        "حرکت موس رو 1:1 و قابل پیش‌بینی می‌کنه (Enhance Pointer Precision خاموش) — ضروری برای شوترها.",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("audio_enhancements_off",
        r"HKCU\Software\Microsoft\Multimedia\Audio", "UserDuckingPreference", 3, 1)
    tweaks.append(Tweak("audio_enhancements_off", "غیرفعال‌سازی Audio Ducking",
        "کم‌شدن خودکار صدای گیم هنگام چت صوتی/تماس رو خاموش می‌کنه.",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("cleartype_on",
        r"HKCU\Control Panel\Desktop", "FontSmoothing", "2", "0", rtype="REG_SZ")
    tweaks.append(Tweak("cleartype_on", "فعال‌سازی ClearType",
        "شارپ‌تر شدن رندر فونت‌ها برای ریدینگ راحت‌تر HUD/متن بازی‌ها.",
        a, r, c, RISK_SAFE))

    return tweaks
