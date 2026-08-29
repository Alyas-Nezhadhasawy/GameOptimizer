"""
GPU vendor guides.
-------------------
Most of the "best settings" for NVIDIA/AMD/Intel live INSIDE each vendor's own
control panel (NVIDIA Control Panel / AMD Software / Intel Graphics Command
Center) — there's no safe, documented registry path for most of them, so
fabricating one would risk breaking someone's driver. Instead this gives an
accurate step-by-step guide per vendor, plus a button that tries to launch
that vendor's control panel directly.
"""

GUIDES = {
    "nvidia": {
        "fa": {
            "title": "NVIDIA Control Panel — بهترین تنظیمات",
            "launch_hint": "برای باز کردن: روی دسکتاپ راست‌کلیک کن → NVIDIA Control Panel، یا از این تب.",
            "steps": [
                "Manage 3D Settings → Power Management Mode = Prefer Maximum Performance",
                "Manage 3D Settings → Low Latency Mode = Ultra (یا On اگه بازیت پشتیبانی نمی‌کنه)",
                "Manage 3D Settings → Texture Filtering - Quality = Performance",
                "Manage 3D Settings → Vertical Sync = Off (مگراینکه Screen Tearing اذیتت کنه)",
                "Manage 3D Settings → Threaded Optimization = On",
                "Display → Adjust Desktop Color Settings → Output Dynamic Range = Full",
                "برای بازی خاص: تب Program Settings → همون بازی رو انتخاب کن و پروفایل جدا بساز",
            ],
        },
        "en": {
            "title": "NVIDIA Control Panel — Best Settings",
            "launch_hint": "To open: right-click desktop → NVIDIA Control Panel, or use the button below.",
            "steps": [
                "Manage 3D Settings → Power Management Mode = Prefer Maximum Performance",
                "Manage 3D Settings → Low Latency Mode = Ultra (or On if your game doesn't support it)",
                "Manage 3D Settings → Texture Filtering - Quality = Performance",
                "Manage 3D Settings → Vertical Sync = Off (unless screen tearing bothers you)",
                "Manage 3D Settings → Threaded Optimization = On",
                "Display → Adjust Desktop Color Settings → Output Dynamic Range = Full",
                "Per-game: Program Settings tab → select the game and create its own profile",
            ],
        },
        "launch_cmd": ["nvcplui.exe"],
    },
    "amd": {
        "fa": {
            "title": "AMD Software (Radeon) — بهترین تنظیمات",
            "launch_hint": "برای باز کردن: راست‌کلیک روی دسکتاپ → AMD Software، یا از این تب.",
            "steps": [
                "Gaming → Graphics → Radeon Anti-Lag = On (برای بازی‌های رقابتی)",
                "Gaming → Graphics → Radeon Chill = Off (برای حداکثر FPS، نه صرفه‌جویی)",
                "Gaming → Graphics → Radeon Boost = On (برای شوترهای رقابتی مفیده)",
                "Gaming → Graphics → Image Sharpening = روشن با مقدار متوسط",
                "Performance → Tuning → Power Efficiency = Off (برای حداکثر عملکرد)",
                "Display → AMD FreeSync = On اگه مانیتورت پشتیبانی می‌کنه",
                "برای بازی خاص: تب Gaming → همون بازی رو انتخاب کن و پروفایل جدا بساز",
            ],
        },
        "en": {
            "title": "AMD Software (Radeon) — Best Settings",
            "launch_hint": "To open: right-click desktop → AMD Software, or use the button below.",
            "steps": [
                "Gaming → Graphics → Radeon Anti-Lag = On (for competitive games)",
                "Gaming → Graphics → Radeon Chill = Off (for max FPS, not power saving)",
                "Gaming → Graphics → Radeon Boost = On (useful for competitive shooters)",
                "Gaming → Graphics → Image Sharpening = On, medium strength",
                "Performance → Tuning → Power Efficiency = Off (for maximum performance)",
                "Display → AMD FreeSync = On if your monitor supports it",
                "Per-game: Gaming tab → select the game and create its own profile",
            ],
        },
        "launch_cmd": ["RadeonSoftware.exe"],
    },
    "intel": {
        "fa": {
            "title": "Intel Graphics Command Center — بهترین تنظیمات",
            "launch_hint": "برای باز کردن: از استارت منو Intel Graphics Command Center رو سرچ کن.",
            "steps": [
                "3D → Preferred Performance State = Maximum Performance",
                "3D → Anisotropic Filtering = Application Controlled یا 16x",
                "3D → Vertical Sync = Application Controlled",
                "Display → Custom Resolutions → مطمئن شو رفرش‌ریت مانیتور روی حداکثر تنظیمه",
                "Power → روی حالت AC، Plugged In performance رو Maximum بذار",
            ],
        },
        "en": {
            "title": "Intel Graphics Command Center — Best Settings",
            "launch_hint": "To open: search 'Intel Graphics Command Center' in the Start menu.",
            "steps": [
                "3D → Preferred Performance State = Maximum Performance",
                "3D → Anisotropic Filtering = Application Controlled or 16x",
                "3D → Vertical Sync = Application Controlled",
                "Display → Custom Resolutions → make sure the monitor refresh rate is set to max",
                "Power → on AC power, set Plugged In performance to Maximum",
            ],
        },
        "launch_cmd": ["IntelGraphicsCommandCenter.exe"],
    },
}


def detect_vendor_hint(gpu_name: str) -> str:
    name = (gpu_name or "").lower()
    if "nvidia" in name or "geforce" in name or "rtx" in name or "gtx" in name:
        return "nvidia"
    if "amd" in name or "radeon" in name:
        return "amd"
    if "intel" in name or "iris" in name or "arc" in name:
        return "intel"
    return "nvidia"
