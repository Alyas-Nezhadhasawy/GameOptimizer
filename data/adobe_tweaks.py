from core.tweak_base import Tweak, RISK_SAFE
from data._helpers import service_toggle, reg_toggle


def build():
    tweaks = []

    # Creative Cloud background autostart processes
    for svc_name, label in [
        ("AdobeUpdateService", "Adobe Update Service"),
        ("CCXProcess", "Creative Cloud Helper (CCXProcess)"),
    ]:
        a, r, c = service_toggle(svc_name)
        tweaks.append(Tweak(f"adobe_{svc_name}", f"غیرفعال‌سازی {label}",
            "از اجرای خودکار Creative Cloud در پس‌زمینه و مصرف RAM/CPU جلوگیری می‌کنه.",
            a, r, c, RISK_SAFE))

    a, r, c = reg_toggle("premiere_gpu_accel",
        r"HKCU\Software\Adobe\Premiere Pro\17.0\Codecs",
        "EnableGPUAcceleration", 1, 0)
    tweaks.append(Tweak("premiere_gpu_accel", "فعال‌سازی GPU Acceleration در Premiere Pro",
        "رندر و پیش‌نمایش تایم‌لاین رو از CPU به GPU منتقل می‌کنه (نسخه‌ی برنامه رو قبل از اعمال چک کن).",
        a, r, c, RISK_SAFE))

    return tweaks
