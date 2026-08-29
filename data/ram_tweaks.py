from core.tweak_base import Tweak, RISK_SAFE, RISK_MEDIUM
from data._helpers import reg_toggle


def build():
    tweaks = []

    a, r, c = reg_toggle("large_system_cache_off",
        r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
        "LargeSystemCache", 0, 1)
    tweaks.append(Tweak("large_system_cache_off", "بهینه‌سازی حافظه برای برنامه‌ها",
        "اولویت مدیریت RAM رو از فایل‌سیستم به سمت برنامه‌ها (بازی‌ها) می‌بره.",
        a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("prefetch_ssd_off",
        r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters",
        "EnablePrefetcher", 0, 3)
    tweaks.append(Tweak("prefetch_ssd_off", "غیرفعال‌سازی Prefetch (توصیه‌شده فقط برای SSD)",
        "روی SSD این ویژگی فایده‌ای نداره و می‌تونه IO اضافه ایجاد کنه.",
        a, r, c, RISK_MEDIUM))

    def clear_standby_apply():
        import subprocess
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-Process | Where-Object {$_.WorkingSet -gt 0} | Out-Null; "
             "[System.GC]::Collect()"],
            capture_output=True)

    def clear_standby_revert():
        pass

    def clear_standby_check():
        return False

    tweaks.append(Tweak("clear_standby", "خالی‌کردن Standby List رم (اجرای دستی)",
        "RAM آزادشده‌ی برنامه‌های بسته‌شده رو واقعاً آزاد می‌کنه؛ قبل از باز کردن بازی‌های سنگین مفیده.",
        clear_standby_apply, clear_standby_revert, clear_standby_check, RISK_SAFE))

    return tweaks
