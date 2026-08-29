from core.tweak_base import Tweak, RISK_SAFE, RISK_MEDIUM
from data._helpers import service_toggle

# (service_name, Persian display name, description, risk)
SERVICES = [
    ("Spooler", "Print Spooler", "اگه پرینتر متصل نداری، بی‌خطر خاموش می‌شه.", RISK_SAFE),
    ("Fax", "Fax Service", "سرویس فکس - امروزه تقریباً هیچ‌کس ازش استفاده نمی‌کنه.", RISK_SAFE),
    ("SysMain", "SysMain (Superfetch)", "روی سیستم‌های با SSD معمولاً فایده‌ای نداره و IO مصرف می‌کنه.", RISK_MEDIUM),
    ("WSearch", "Windows Search", "ایندکس‌گذاری فایل‌ها؛ خاموش کردنش جستجوی فایل رو کندتر می‌کنه ولی IO آزاد می‌کنه.", RISK_MEDIUM),
    ("bthserv", "Bluetooth Support", "اگه دستگاه بلوتوث استفاده نمی‌کنی.", RISK_SAFE),
    ("DiagTrack", "Connected User Experiences and Telemetry", "تله‌متری/ارسال دیتای مصرف به مایکروسافت.", RISK_SAFE),
    ("RemoteRegistry", "Remote Registry", "دسترسی از راه دور به رجیستری - برای اکثر کاربران خانگی غیرضروریه.", RISK_SAFE),
]


def build():
    tweaks = []
    for name, label, desc, risk in SERVICES:
        a, r, c = service_toggle(name)
        tweaks.append(Tweak(f"svc_{name}", label, desc, a, r, c, risk))
    return tweaks
