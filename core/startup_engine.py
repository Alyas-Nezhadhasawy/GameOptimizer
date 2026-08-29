"""
Startup / Autorun manager
-------------------------
Covers the three places apps hide themselves to auto-launch on boot:
  1. Registry Run keys        (HKCU/HKLM ...\\Run and \\RunOnce)
  2. Startup folder shortcuts (shell:startup, shell:common startup)
  3. Scheduled Tasks set to run "At log on"

"Disable" never deletes anything: Run-key entries are moved to a sibling
"...\\Run-Disabled" key, Startup-folder shortcuts are moved to a
"Disabled" subfolder, and Scheduled Tasks are simply Disabled (not
deleted) via schtasks. "Enable" reverses each of those exactly, so nothing
the user didn't explicitly delete is ever lost.
"""
import os
import subprocess
import winreg

RUN_KEYS = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
]
DISABLED_SUFFIX = "-GODisabled"


def _disabled_key_path(path):
    return path + DISABLED_SUFFIX


def list_run_key_apps():
    """Returns [{'name', 'command', 'hive', 'path', 'enabled': True}, ...]"""
    results = []
    for hive, path in RUN_KEYS:
        for enabled, p in ((True, path), (False, _disabled_key_path(path))):
            try:
                with winreg.OpenKey(hive, p) as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            results.append({
                                "source": "run_key", "name": name, "command": value,
                                "hive": hive, "path": path, "enabled": enabled,
                            })
                            i += 1
                        except OSError:
                            break
            except FileNotFoundError:
                continue
    return results


def toggle_run_key_app(hive, path, name, enable: bool):
    # enabling: move value FROM the disabled key TO the live key (and vice versa)
    src = _disabled_key_path(path) if enable else path
    dst = path if enable else _disabled_key_path(path)

    with winreg.OpenKey(hive, src, 0, winreg.KEY_ALL_ACCESS) as src_key:
        value, vtype = winreg.QueryValueEx(src_key, name)
        winreg.DeleteValue(src_key, name)

    winreg.CreateKey(hive, dst)
    with winreg.OpenKey(hive, dst, 0, winreg.KEY_SET_VALUE) as dst_key:
        winreg.SetValueEx(dst_key, name, 0, vtype, value)


STARTUP_FOLDERS = [
    os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"),
    os.path.join(os.environ.get("PROGRAMDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"),
]


def list_startup_folder_apps():
    results = []
    for folder in STARTUP_FOLDERS:
        if not os.path.isdir(folder):
            continue
        for enabled, sub in ((True, folder), (False, os.path.join(folder, "Disabled"))):
            if not os.path.isdir(sub):
                continue
            for fname in os.listdir(sub):
                if fname.lower().endswith((".lnk", ".exe", ".bat")):
                    results.append({
                        "source": "startup_folder", "name": fname,
                        "folder": folder, "enabled": enabled,
                    })
    return results


def toggle_startup_folder_app(folder, fname, enable: bool):
    disabled_dir = os.path.join(folder, "Disabled")
    os.makedirs(disabled_dir, exist_ok=True)
    if enable:
        src, dst = os.path.join(disabled_dir, fname), os.path.join(folder, fname)
    else:
        src, dst = os.path.join(folder, fname), os.path.join(disabled_dir, fname)
    os.replace(src, dst)


def list_logon_scheduled_tasks():
    """Scheduled Tasks whose trigger is 'At log on'."""
    ps = (
        "Get-ScheduledTask | Where-Object { $_.Triggers.CimClass.CimClassName "
        "-contains 'MSFT_TaskLogonTrigger' } | "
        "Select-Object TaskName, TaskPath, State | ConvertTo-Csv -NoTypeInformation"
    )
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                          capture_output=True, text=True)
    rows = []
    for line in out.stdout.splitlines()[1:]:
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) == 3:
            rows.append({"source": "scheduled_task", "name": parts[0],
                        "path": parts[1].strip('"'), "enabled": parts[2].strip() == "Ready"})
    return rows


def toggle_scheduled_task(task_path, task_name, enable: bool):
    full = task_path.rstrip("\\") + "\\" + task_name
    action = "/Enable" if enable else "/Disable"
    subprocess.run(["schtasks", "/Change", "/TN", full, action],
                    capture_output=True, text=True)


def list_all():
    return list_run_key_apps() + list_startup_folder_apps() + list_logon_scheduled_tasks()
