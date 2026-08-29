"""Admin elevation + system helpers (Windows only)."""
import ctypes
import sys
import subprocess


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def relaunch_as_admin():
    """Re-launch the current script/exe with elevated (UAC) rights."""
    params = " ".join([f'"{a}"' for a in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 1
    )
    sys.exit(0)


def ensure_admin():
    if not is_admin():
        relaunch_as_admin()


def create_restore_point(description: str = "GamingOptimizer - Before Tweaks"):
    """Creates a Windows System Restore Point via PowerShell (System Protection must be ON)."""
    ps_cmd = (
        f'Checkpoint-Computer -Description "{description}" '
        f'-RestorePointType "MODIFY_SETTINGS"'
    )
    return subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_cmd],
        capture_output=True, text=True
    )


def enable_system_protection():
    """Makes sure System Restore is enabled on C: before trying to create a point."""
    ps_cmd = 'Enable-ComputerRestore -Drive "C:\\"'
    return subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_cmd],
        capture_output=True, text=True
    )
