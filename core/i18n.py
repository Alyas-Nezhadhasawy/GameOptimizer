"""
Minimal i18n layer.
-------------------
Language is picked ONCE on the splash screen, before MainWindow (and every
tab) is built — so nothing needs to re-render mid-session. Every tab reads
strings through t("key") at construction time.

Tweak name/description stay in Persian on the Tweak object itself (that's
the canonical copy, unchanged from before); English overrides live in
TWEAK_EN below and are looked up through tweak_name()/tweak_desc() so nothing
about core/data files had to change.
"""

LANG = "fa"


def set_lang(lang: str):
    global LANG
    LANG = lang if lang in ("fa", "en") else "fa"


def t(key: str) -> str:
    return CHROME.get(LANG, CHROME["fa"]).get(key, CHROME["fa"].get(key, key))


def tweak_name(tweak) -> str:
    if LANG == "en" and tweak.id in TWEAK_EN:
        return TWEAK_EN[tweak.id][0]
    return tweak.name


def tweak_desc(tweak) -> str:
    if LANG == "en" and tweak.id in TWEAK_EN:
        return TWEAK_EN[tweak.id][1]
    return tweak.description


CHROME = {
    "fa": {
        "app_title": "⚡ Gaming Optimizer",
        "window_title": "Gaming Optimizer",
        "apply_selected": "اعمال موارد انتخاب‌شده",
        "restore_default": "بازگردانی به حالت پیش‌فرض",
        "scanning": "در حال بررسی وضعیت فعلی سیستم...",
        "scanned": "✅ وضعیت فعلی سیستم بررسی شد — مواردی که قبلاً (چه با این برنامه، چه دستی) انجام شده بودن به‌صورت خودکار تیک خوردن.",
        "risk_safe": "بی‌خطر", "risk_medium": "متوسط", "risk_high": "پرریسک",
        "ok": "باشه", "error_title": "خطا", "rescan": "🔄 اسکن مجدد",

        "start_title": "Start", "start_subtitle": "قبل از هر تغییری، از سیستم بک‌آپ بگیر.",
        "backup_section": "۱) بک‌آپ / Restore Point", "backup_not_yet": "هنوز بک‌آپ گرفته نشده.",
        "backup_btn": "ساخت System Restore Point + Export رجیستری",
        "debloat_section": "۲) حذف برنامه‌های غیرقابل‌استفاده", "debloat_btn": "حذف موارد انتخاب‌شده",
        "update_section": "۳) غیرفعال‌سازی Windows Update", "update_checking": "در حال بررسی وضعیت فعلی...",
        "update_btn": "غیرفعال کن",

        "cleanup_title": "Clean Up", "cleanup_subtitle": "فضای دیسک آزاد می‌کنه و سرعت لود ویندوز رو بهتر می‌کنه.",
        "cleanup_btn": "پاکسازی موارد انتخاب‌شده", "cleanup_disk_btn": "اجرای Disk Cleanup ویندوز (cleanmgr)",

        "startup_title": "Startup / Autorun Apps",
        "startup_subtitle": "برنامه‌هایی که مخفیانه با ویندوز اجرا می‌شن — روشن/خاموش کن، هیچی حذف نمی‌شه.",
        "startup_scanning": "در حال اسکن Registry، پوشه‌ی Startup و Task Scheduler...",
        "startup_none": "هیچ برنامه‌ی Autorun پیدا نشد.",

        "msi_title": "MSI Mode Tools",
        "msi_subtitle": "تبدیل وقفه‌های سخت‌افزاری از Line-Based به MSI برای لتنسی پایین‌تر.",
        "msi_rescan": "🔄 اسکن مجدد دستگاه‌ها", "msi_none": "دستگاهی در این دسته پیدا نشد.",
        "msi_no_param": "(این دستگاه پارامتر MSI رو نداره)",
        "cat_gpu": "کارت گرافیک", "cat_storage": "درایو ذخیره‌سازی", "cat_network": "کارت شبکه", "cat_usb": "کنترلر USB",

        "priority_title": "Game High Priority",
        "priority_subtitle": "اولویت CPU بازی رو دائمی روی High/Real-time تنظیم کن — یک‌بار تنظیم، همیشه فعال.",
        "priority_placeholder": "مثلاً: valorant.exe یا fortniteclient-win64-shipping.exe",
        "priority_browse": "انتخاب فایل exe...", "priority_apply": "اعمال مستقیم روی سیستم",
        "priority_export": "ساخت فایل GameHighPriority.reg", "priority_configured": "بازی‌های فعلاً تنظیم‌شده:",

        "gpu_setting_title": "GPU Setting", "gpu_setting_subtitle": "تنظیمات اولیه و پایه‌ی درایور گرافیک، مستقل از برند.",
        "gpu_detecting": "در حال شناسایی کارت گرافیک...", "gpu_detected": "کارت گرافیک شناسایی‌شده:",

        "gpu_vendor_title": "راهنمای اختصاصی کارت گرافیک",
        "gpu_vendor_subtitle": "برند کارت گرافیکت رو انتخاب کن تا بهترین تنظیمات پیشنهادی رو ببینی.",
        "gpu_vendor_open_panel": "باز کردن کنترل پنل درایور",

        "games_title": "Game Presets", "games_subtitle": "روی بازی موردنظرت کلیک کن تا بهترین تنظیمات رو ببینی.",
        "games_search": "جستجوی بازی...", "games_apply_recommended": "اعمال تنظیمات پیشنهادی سیستم",
        "games_go_priority": "رفتن به تب Game High Priority",
        "games_settings_for": "بهترین تنظیمات پیشنهادی برای",

        "splash_choose_lang": "زبان را انتخاب کنید / Choose your language",
        "splash_loading": "در حال بارگذاری برنامه...",
    },
    "en": {
        "app_title": "⚡ Gaming Optimizer",
        "window_title": "Gaming Optimizer",
        "apply_selected": "Apply Selected",
        "restore_default": "Restore Defaults",
        "scanning": "Scanning current system state...",
        "scanned": "✅ Current system state scanned — anything already done (by this app or manually) is auto-checked.",
        "risk_safe": "Safe", "risk_medium": "Medium", "risk_high": "High Risk",
        "ok": "OK", "error_title": "Error", "rescan": "🔄 Rescan",

        "start_title": "Start", "start_subtitle": "Back up your system before changing anything.",
        "backup_section": "1) Backup / Restore Point", "backup_not_yet": "No backup taken yet.",
        "backup_btn": "Create System Restore Point + Registry Export",
        "debloat_section": "2) Remove Unused Apps", "debloat_btn": "Remove Selected",
        "update_section": "3) Disable Windows Update", "update_checking": "Checking current state...",
        "update_btn": "Disable",

        "cleanup_title": "Clean Up", "cleanup_subtitle": "Frees disk space and speeds up Windows boot.",
        "cleanup_btn": "Clean Selected", "cleanup_disk_btn": "Run Windows Disk Cleanup (cleanmgr)",

        "startup_title": "Startup / Autorun Apps",
        "startup_subtitle": "Apps that silently launch with Windows — flip the switch, nothing gets deleted.",
        "startup_scanning": "Scanning Registry, Startup folder and Task Scheduler...",
        "startup_none": "No autorun apps found.",

        "msi_title": "MSI Mode Tools",
        "msi_subtitle": "Switch hardware interrupts from line-based to MSI for lower latency.",
        "msi_rescan": "🔄 Rescan Devices", "msi_none": "No devices found in this category.",
        "msi_no_param": "(this device has no MSI parameter)",
        "cat_gpu": "Graphics Card", "cat_storage": "Storage Drive", "cat_network": "Network Card", "cat_usb": "USB Controller",

        "priority_title": "Game High Priority",
        "priority_subtitle": "Permanently set a game's CPU priority to High/Real-time — set once, always on.",
        "priority_placeholder": "e.g. valorant.exe or fortniteclient-win64-shipping.exe",
        "priority_browse": "Browse for .exe...", "priority_apply": "Apply Directly to System",
        "priority_export": "Generate GameHighPriority.reg", "priority_configured": "Currently configured games:",

        "gpu_setting_title": "GPU Setting", "gpu_setting_subtitle": "Baseline graphics driver settings, vendor-independent.",
        "gpu_detecting": "Detecting graphics card...", "gpu_detected": "Detected GPU:",

        "gpu_vendor_title": "GPU Vendor Guide",
        "gpu_vendor_subtitle": "Pick your GPU brand to see the best recommended settings.",
        "gpu_vendor_open_panel": "Open Driver Control Panel",

        "games_title": "Game Presets", "games_subtitle": "Click a game to see its best recommended settings.",
        "games_search": "Search games...", "games_apply_recommended": "Apply Recommended System Tweaks",
        "games_go_priority": "Go to Game High Priority tab",
        "games_settings_for": "Best recommended settings for",

        "splash_choose_lang": "زبان را انتخاب کنید / Choose your language",
        "splash_loading": "Loading application...",
    },
}

# tweak_id -> (name_en, description_en)
TWEAK_EN = {
    "sys_responsiveness": ("Lower SystemResponsiveness",
        "Gives foreground apps (games) a bigger share of CPU instead of background tasks."),
    "network_throttling": ("Disable Network Throttling",
        "Removes the network packet processing cap to reduce lag in online games."),
    "priority_separation": ("Tune Win32PrioritySeparation",
        "Biases CPU scheduling toward the active app (game) with a fixed quantum."),
    "gamedvr_off": ("Disable Game DVR",
        "Turns off Xbox Game Bar's background recording, which can hurt FPS and cause stutter."),
    "core_isolation": ("Disable Core Isolation / Memory Integrity",
        "Can gain a few % FPS, but turns off a Windows security layer. Advanced users only."),
    "hpet_bcd": ("Disable HPET / Dynamic Tick (BCD)",
        "Tunes the system timer to reduce micro-stutter and small in-game lag spikes. Requires a restart."),

    "visual_fx_perf": ("Visual Effects: Best Performance",
        "Turns off unnecessary Windows animations and visual effects."),
    "transparency_off": ("Disable Transparency",
        "Turns off the taskbar/menu transparency effect (slightly less GPU usage)."),
    "game_bar_off": ("Enable Auto Game Mode",
        "Forces Windows to prioritize resources while a game is running."),
    "hibernate_off": ("Disable Hibernation",
        "Removes hiberfil.sys (several GB) and lightens boot slightly."),
    "storage_sense_on": ("Enable Storage Sense",
        "Automatically and periodically frees up disk space."),

    "mouse_accel_off": ("Disable Mouse Acceleration",
        "Makes mouse movement 1:1 and predictable (Enhance Pointer Precision off) — essential for shooters."),
    "audio_enhancements_off": ("Disable Audio Ducking",
        "Turns off automatic game-volume reduction during voice chat/calls."),
    "cleartype_on": ("Enable ClearType",
        "Sharper font rendering for easier reading of in-game HUD/text."),

    "svc_Spooler": ("Disable Print Spooler", "Safe to disable if you have no printer connected."),
    "svc_Fax": ("Disable Fax Service", "Almost nobody uses fax anymore."),
    "svc_SysMain": ("Disable SysMain (Superfetch)", "Usually pointless on SSDs and consumes IO."),
    "svc_WSearch": ("Disable Windows Search", "Slower file search, but frees up IO."),
    "svc_bthserv": ("Disable Bluetooth Support", "If you don't use any Bluetooth devices."),
    "svc_DiagTrack": ("Disable Telemetry Service", "Usage-data collection sent to Microsoft."),
    "svc_RemoteRegistry": ("Disable Remote Registry", "Remote registry access — unneeded for most home users."),

    "nagle_off": ("Disable Nagle's Algorithm",
        "Reduces small-TCP-packet send delay — steadier ping in online games."),
    "net_throttle_off": ("Remove Multimedia Bandwidth Cap",
        "Removes the network processing ceiling Windows sets for multimedia apps."),
    "dns_cloudflare": ("Set DNS to Cloudflare (1.1.1.1)",
        "Faster/more stable than most default ISP DNS in most regions. Check your adapter name before applying."),

    "large_system_cache_off": ("Optimize Memory for Applications",
        "Shifts RAM management priority from the filesystem toward apps (games)."),
    "prefetch_ssd_off": ("Disable Prefetch (recommended for SSD only)",
        "Pointless on an SSD and can add extra IO."),
    "clear_standby": ("Clear RAM Standby List (manual run)",
        "Actually frees RAM held by closed apps; useful before launching a heavy game."),

    "adobe_AdobeUpdateService": ("Disable Adobe Update Service", "Stops Creative Cloud auto-updating in the background."),
    "adobe_CCXProcess": ("Disable Creative Cloud Helper", "Stops the CC background helper from auto-starting."),
    "premiere_gpu_accel": ("Enable GPU Acceleration in Premiere Pro",
        "Moves timeline rendering/preview from CPU to GPU (check your app version before applying)."),

    "hags_on": ("Enable Hardware-Accelerated GPU Scheduling",
        "Moves GPU queue scheduling from the driver to the GPU itself; can lower latency on some systems."),
    "tdr_delay": ("Increase TDR Delay",
        "Prevents the graphics driver from restarting during heavy renders/overclocks (fewer crashes, not more speed)."),
    "fso_off": ("Disable Fullscreen Optimizations (global)",
        "Some games run smoother in true Exclusive Fullscreen than Windows' optimized mode."),

    "gpu_pref_max_perf": ("Enable SwapEffect Upgrade",
        "Forces some older games to use newer presentation models (lower latency)."),
    "tdr_level": ("Restore Default TDR Level (driver stability)",
        "Makes sure Timeout Detection & Recovery is on the standard setting."),

    "ultimate_perf": ("Enable Ultimate Performance Power Plan",
        "Windows' hidden plan that disables all energy-saving throttling."),
    "usb_selective_suspend": ("Disable USB Selective Suspend",
        "Prevents USB devices (mouse/controller/headset) from sleeping when idle."),
    "cpu_min_max_100": ("Lock CPU to Max Power State (Min/Max = 100%)",
        "Prevents CPU frequency dips between frames; note: raises idle temperature."),
}
