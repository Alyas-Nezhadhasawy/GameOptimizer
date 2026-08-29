"""Windows service start-type control, with backup of the previous start type."""
import subprocess
import json
import os

from .registry_engine import BACKUP_DIR

START_TYPE_MAP = {
    "boot": 0, "system": 1, "auto": 2, "manual": 3, "disabled": 4,
}


def get_start_type(service_name: str) -> str:
    out = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         f"(Get-Service -Name '{service_name}' -ErrorAction SilentlyContinue) | Out-Null; "
         f"(Get-WmiObject Win32_Service -Filter \"Name='{service_name}'\").StartMode"],
        capture_output=True, text=True
    )
    return out.stdout.strip().lower()  # "auto", "manual", "disabled"


def set_start_type(service_name: str, new_type: str, tweak_id: str = "unknown"):
    """new_type is one of: automatic, manual, disabled"""
    old_type = get_start_type(service_name)
    _backup_service_state(tweak_id, service_name, old_type)
    subprocess.run(
        ["sc", "config", service_name, "start=", new_type],
        capture_output=True, text=True
    )
    if new_type == "disabled":
        subprocess.run(["sc", "stop", service_name], capture_output=True, text=True)


def _backup_service_state(tweak_id, service_name, old_type):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    fname = os.path.join(BACKUP_DIR, "service_backups.json")
    data = {}
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    data[service_name] = {"tweak_id": tweak_id, "old_type": old_type}
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def restore_service(service_name: str):
    fname = os.path.join(BACKUP_DIR, "service_backups.json")
    if not os.path.exists(fname):
        return False
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    entry = data.get(service_name)
    if not entry:
        return False
    old_type = entry["old_type"] or "manual"
    subprocess.run(["sc", "config", service_name, "start=", old_type],
                    capture_output=True, text=True)
    if old_type in ("auto", "automatic"):
        subprocess.run(["sc", "start", service_name], capture_output=True, text=True)
    return True
