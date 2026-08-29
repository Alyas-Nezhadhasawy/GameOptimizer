import customtkinter as ctk
from core.powershell_bridge import run_powercfg
from data._helpers import reg_toggle
from core.tweak_base import Tweak, RISK_SAFE
from ui.generic_tweak_tab import GenericTweakTab

# GUID of Windows' built-in "Ultimate Performance" plan (hidden by default)
ULTIMATE_PERF_GUID = "e9a42b02-d5df-448d-aa00-03f14749eb61"


def _build_tweaks():
    tweaks = []

    def apply_ultimate():
        run_powercfg(f"-duplicatescheme {ULTIMATE_PERF_GUID}")
        run_powercfg(f"-setactive {ULTIMATE_PERF_GUID}")

    def revert_ultimate():
        run_powercfg("-setactive SCHEME_BALANCED")

    def check_ultimate():
        out = run_powercfg("/getactivescheme")
        return ULTIMATE_PERF_GUID.lower() in (out.stdout or "").lower()

    tweaks.append(Tweak("ultimate_perf", "فعال‌سازی پاورپلن Ultimate Performance",
        "پلن مخفی ویندوز که همه‌ی throttlingهای صرفه‌جویی انرژی رو غیرفعال می‌کنه.",
        apply_ultimate, revert_ultimate, check_ultimate, RISK_SAFE))

    a, r, c = reg_toggle("usb_selective_suspend",
        r"HKLM\SYSTEM\CurrentControlSet\Control\Power",
        "USBSelectiveSuspendPolicy", 0, 1)
    tweaks.append(Tweak("usb_selective_suspend", "غیرفعال‌سازی USB Selective Suspend",
        "از خواب‌رفتن دستگاه‌های USB (موس/دسته/هدست) هنگام بی‌کاری جلوگیری می‌کنه.",
        a, r, c, RISK_SAFE))

    def cpu_min_max_apply():
        run_powercfg("-setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 100")
        run_powercfg("-setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100")
        run_powercfg("-setactive SCHEME_CURRENT")

    def cpu_min_max_revert():
        run_powercfg("-setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5")
        run_powercfg("-setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100")

    def cpu_min_max_check():
        out = run_powercfg("-getacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN")
        text = out.stdout or ""
        # powercfg prints "Current AC Power Setting Index: 0x00000064" (100 decimal) when at 100%
        return "0x00000064" in text

    tweaks.append(Tweak("cpu_min_max_100", "قفل کردن CPU روی حداکثر توان (Min/Max State = 100%)",
        "از افت فرکانس CPU بین فریم‌ها جلوگیری می‌کنه؛ توجه: دمای بی‌کاری سیستم رو بالا می‌بره.",
        cpu_min_max_apply, cpu_min_max_revert, cpu_min_max_check, RISK_SAFE))

    return tweaks


class PowerPlanTab(GenericTweakTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Power Plan",
                          "مصرف برق، توان و دمای سیستم رو برای گیمینگ بهینه کن.",
                          _build_tweaks(), **kwargs)
