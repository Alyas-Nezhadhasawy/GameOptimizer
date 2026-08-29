"""
Registry Engine
---------------
Every write goes through this module so that:
  1. The previous value is captured first (into a JSON backup file).
  2. The write can later be reverted exactly (including "the value didn't exist").
This is what makes every tab's "Restore Default" button work.
"""
import json
import os
import datetime

try:
    import winreg
except ImportError:
    winreg = None  # allows the file to be imported/inspected on non-Windows for review

BACKUP_DIR = os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
                           "GamingOptimizer", "backups")

_HIVES = {
    "HKLM": getattr(winreg, "HKEY_LOCAL_MACHINE", None),
    "HKCU": getattr(winreg, "HKEY_CURRENT_USER", None),
    "HKCR": getattr(winreg, "HKEY_CLASSES_ROOT", None),
    "HKU": getattr(winreg, "HKEY_USERS", None),
}

_TYPES = {
    "REG_SZ": getattr(winreg, "REG_SZ", 1),
    "REG_DWORD": getattr(winreg, "REG_DWORD", 4),
    "REG_QWORD": getattr(winreg, "REG_QWORD", 11),
    "REG_BINARY": getattr(winreg, "REG_BINARY", 3),
    "REG_EXPAND_SZ": getattr(winreg, "REG_EXPAND_SZ", 2),
    "REG_MULTI_SZ": getattr(winreg, "REG_MULTI_SZ", 7),
}


def _split(full_path: str):
    hive_name, path = full_path.split("\\", 1)
    return _HIVES[hive_name], path


def read_value(full_path: str, value_name: str):
    """Returns (value, type) or (None, None) if the key/value doesn't exist."""
    hive, path = _split(full_path)
    try:
        with winreg.OpenKey(hive, path, 0, winreg.KEY_READ) as key:
            val, vtype = winreg.QueryValueEx(key, value_name)
            return val, vtype
    except FileNotFoundError:
        return None, None


def write_value(full_path: str, value_name: str, value, reg_type: str = "REG_DWORD",
                 tweak_id: str = "unknown"):
    """Writes a value, auto-backing up whatever was there before under tweak_id."""
    hive, path = _split(full_path)
    old_val, old_type = read_value(full_path, value_name)
    _backup_entry(tweak_id, full_path, value_name, old_val, old_type)

    winreg.CreateKey(hive, path)  # ensures the key chain exists
    with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, value_name, 0, _TYPES[reg_type], value)


def delete_value(full_path: str, value_name: str, tweak_id: str = "unknown"):
    hive, path = _split(full_path)
    old_val, old_type = read_value(full_path, value_name)
    if old_val is None:
        return
    _backup_entry(tweak_id, full_path, value_name, old_val, old_type)
    try:
        with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, value_name)
    except FileNotFoundError:
        pass


def _backup_entry(tweak_id, full_path, value_name, old_val, old_type):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    fname = os.path.join(BACKUP_DIR, "registry_backups.json")
    data = {}
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    data.setdefault(tweak_id, [])
    data[tweak_id].append({
        "path": full_path,
        "name": value_name,
        "value": old_val,
        "type": old_type,
        "timestamp": datetime.datetime.now().isoformat(),
    })
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def restore_tweak(tweak_id: str):
    """Re-applies whatever was backed up for this tweak_id, in reverse order (last change first)."""
    fname = os.path.join(BACKUP_DIR, "registry_backups.json")
    if not os.path.exists(fname):
        return False
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    entries = data.get(tweak_id, [])
    for entry in reversed(entries):
        hive, path = _split(entry["path"])
        if entry["value"] is None:
            # it didn't exist before -> delete it now
            try:
                with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteValue(key, entry["name"])
            except FileNotFoundError:
                pass
        else:
            winreg.CreateKey(hive, path)
            with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, entry["name"], 0, entry["type"], entry["value"])
    data[tweak_id] = []
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True


def export_full_registry_backup(dest_path: str):
    """Full HKLM+HKCU export via reg.exe — the real safety net, independent of our JSON backups."""
    import subprocess
    os.makedirs(dest_path, exist_ok=True)
    subprocess.run(["reg", "export", "HKLM", os.path.join(dest_path, "HKLM_backup.reg"), "/y"])
    subprocess.run(["reg", "export", "HKCU", os.path.join(dest_path, "HKCU_backup.reg"), "/y"])
