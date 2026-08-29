from core.tweak_base import Tweak, RISK_SAFE, RISK_MEDIUM
from data._helpers import reg_toggle


def build():
    tweaks = []

    a, r, c = reg_toggle("visual_fx_perf",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
        "VisualFXSetting", 2, 0)
    tweaks.append(Tweak("visual_fx_perf", "Visual Effects روی Best Performance",
        "همه‌ی انیمیشن‌ها و افکت‌های بصری غیرضروری ویندوز رو خاموش می‌کنه.",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("transparency_off",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "EnableTransparency", 0, 1)
    tweaks.append(Tweak("transparency_off", "غیرفعال‌سازی Transparency",
        "افکت شفافیت نوار وظیفه و منوها رو خاموش می‌کنه (کمی مصرف GPU کمتر).",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("game_bar_off",
        r"HKCU\Software\Microsoft\GameBar",
        "AllowAutoGameMode", 1, 0)
    tweaks.append(Tweak("game_bar_off", "فعال‌سازی Auto Game Mode",
        "ویندوز رو مجبور می‌کنه هنگام اجرای بازی منابع رو اولویت‌بندی کنه.",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("hibernate_off",
        r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power",
        "HibernateEnabled", 0, 1)
    tweaks.append(Tweak("hibernate_off", "غیرفعال‌سازی Hibernation",
        "فایل hiberfil.sys (چند گیگ فضا) رو حذف و بوت رو کمی سبک‌تر می‌کنه.",
        a, r, c, RISK_MEDIUM))

    a, r, c = reg_toggle("storage_sense_on",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\StorageSense\Parameters\StoragePolicy",
        "01", 1, 0)
    tweaks.append(Tweak("storage_sense_on", "فعال‌سازی Storage Sense",
        "فضای دیسک رو به‌صورت خودکار و دوره‌ای پاک‌سازی می‌کنه.",
        a, r, c, RISK_SAFE))

    return tweaks
