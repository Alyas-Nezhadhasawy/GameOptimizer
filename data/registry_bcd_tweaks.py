from core.tweak_base import Tweak, RISK_SAFE, RISK_MEDIUM, RISK_HIGH
from core import registry_engine as reg
from core.powershell_bridge import run_bcdedit
from data._helpers import reg_toggle as _reg_toggle


def build():
    tweaks = []

    a, r, c = _reg_toggle(
        "sys_responsiveness",
        r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
        "SystemResponsiveness", 0, 20)
    tweaks.append(Tweak(
        "sys_responsiveness", "کاهش SystemResponsiveness",
        "درصد بیشتری از CPU رو به برنامه فورگراند (بازی) به‌جای پس‌زمینه اختصاص می‌ده.",
        a, r, c, RISK_SAFE))

    a, r, c = _reg_toggle(
        "network_throttling",
        r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
        "NetworkThrottlingIndex", 0xffffffff, 10)
    tweaks.append(Tweak(
        "network_throttling", "غیرفعال‌سازی Network Throttling",
        "محدودیت پردازش پکت‌های شبکه رو برای کاهش لگ آنلاین برمی‌داره.",
        a, r, c, RISK_SAFE))

    a, r, c = _reg_toggle(
        "priority_separation",
        r"HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl",
        "Win32PrioritySeparation", 26, 2)
    tweaks.append(Tweak(
        "priority_separation", "بهینه‌سازی Win32PrioritySeparation",
        "زمان‌بندی CPU رو به نفع برنامه‌ی فعال (بازی) با کوانتوم ثابت تنظیم می‌کنه.",
        a, r, c, RISK_MEDIUM))

    a, r, c = _reg_toggle(
        "gamedvr_off",
        r"HKCU\System\GameConfigStore",
        "GameDVR_Enabled", 0, 1)
    tweaks.append(Tweak(
        "gamedvr_off", "غیرفعال‌سازی Game DVR",
        "ضبط پس‌زمینه‌ی Xbox Game Bar که باعث افت FPS و استاتر می‌شه رو خاموش می‌کنه.",
        a, r, c, RISK_SAFE))

    def core_isolation_apply():
        reg.write_value(
            r"HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity",
            "Enabled", 0, "REG_DWORD", "core_isolation")

    def core_isolation_revert():
        reg.restore_tweak("core_isolation")

    def core_isolation_check():
        v, _ = reg.read_value(
            r"HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity",
            "Enabled")
        return v == 0

    tweaks.append(Tweak(
        "core_isolation", "غیرفعال‌سازی Core Isolation / Memory Integrity",
        "می‌تونه چند درصد FPS بیشتر بده، ولی یک لایه‌ی امنیتی ویندوز رو خاموش می‌کنه. فقط برای کاربران باتجربه.",
        core_isolation_apply, core_isolation_revert, core_isolation_check, RISK_HIGH))

    def hpet_apply():
        run_bcdedit("/deletevalue useplatformclock")
        run_bcdedit("/set disabledynamictick yes")

    def hpet_revert():
        run_bcdedit("/set useplatformclock true")
        run_bcdedit("/set disabledynamictick no")

    def hpet_check():
        out = run_bcdedit("/enum {current}")
        text = (out.stdout or "").lower()
        return "disabledynamictick" in text and "yes" in text.split("disabledynamictick", 1)[1][:20]

    tweaks.append(Tweak(
        "hpet_bcd", "غیرفعال‌سازی HPET / Dynamic Tick (BCD)",
        "تایمر سیستم رو برای کاهش میکرو-استاتر و لگ‌های ریز در گیم بهینه می‌کنه. نیاز به ریستارت داره.",
        hpet_apply, hpet_revert, hpet_check, RISK_MEDIUM))

    return tweaks
