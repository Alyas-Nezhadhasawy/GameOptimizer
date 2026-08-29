from core.tweak_base import Tweak, RISK_SAFE, RISK_MEDIUM
from data._helpers import reg_toggle
from core.powershell_bridge import run_netsh


def build():
    tweaks = []

    def nagle_apply():
        # Nagle's algorithm lives per-interface under Tcpip\Parameters\Interfaces\{GUID}
        # here we set the machine-wide default; per-adapter loop can be added once
        # the target NIC's GUID is known.
        reg_apply, _, _ = reg_toggle(
            "nagle_off",
            r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
            "TcpAckFrequency", 1, 2)
        reg_apply()

    def nagle_revert():
        from core import registry_engine as reg
        reg.restore_tweak("nagle_off")

    def nagle_check():
        from core import registry_engine as reg
        v, _ = reg.read_value(
            r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpAckFrequency")
        return v == 1

    tweaks.append(Tweak("nagle_off", "غیرفعال‌سازی Nagle's Algorithm",
        "تأخیر ارسال پکت‌های کوچک TCP رو کاهش می‌ده - پینگ پایدارتر توی بازی‌های آنلاین.",
        nagle_apply, nagle_revert, nagle_check, RISK_MEDIUM))

    a, r, c = reg_toggle("net_throttle_off",
        r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
        "NetworkThrottlingIndex", 0xffffffff, 10)
    tweaks.append(Tweak("net_throttle_off", "برداشتن محدودیت پهنای باند مالتی‌مدیا",
        "سقف پردازش شبکه که ویندوز برای برنامه‌های مالتی‌مدیا می‌ذاره رو برمی‌داره.",
        a, r, c, RISK_SAFE))

    def _get_active_adapter():
        """Auto-detect the active network adapter name."""
        out = run_netsh('interface show interface')
        for line in (out.stdout or "").splitlines():
            parts = line.split()
            if len(parts) >= 4 and parts[0] == "Enabled" and parts[1] == "Connected":
                return " ".join(parts[3:])
        return "Ethernet"  # fallback

    def dns_apply():
        adapter = _get_active_adapter()
        run_netsh(f'interface ip set dns name="{adapter}" static 1.1.1.1')
        run_netsh(f'interface ip add dns name="{adapter}" 1.0.0.1 index=2')

    def dns_revert():
        adapter = _get_active_adapter()
        run_netsh(f'interface ip set dns name="{adapter}" dhcp')

    def dns_check():
        adapter = _get_active_adapter()
        out = run_netsh(f'interface ip show dns name="{adapter}"')
        return "1.1.1.1" in (out.stdout or "")

    tweaks.append(Tweak("dns_cloudflare", "تنظیم DNS روی Cloudflare (1.1.1.1)",
        "در اکثر مناطق سریع‌تر و پایدارتر از DNS پیش‌فرض ISP هست. آداپتور فعال به‌صورت خودکار شناسایی می‌شه.",
        dns_apply, dns_revert, dns_check, RISK_MEDIUM))

    return tweaks
