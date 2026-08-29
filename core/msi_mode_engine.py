"""
MSI (Message Signaled Interrupts) Mode
---------------------------------------
Switches a PCI/PCIe device (GPU, NVMe, network card...) from legacy
line-based interrupts to MSI mode, which can lower input/audio latency.
Real Windows devices expose this under:

  HKLM\\SYSTEM\\CurrentControlSet\\Enum\\<DeviceInstancePath>\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties
      MSISupported = 1 (DWORD)

We enumerate candidate devices via PowerShell (Get-PnpDevice) rather than
guessing instance paths.
"""
import subprocess
import winreg

CATEGORY_CLASSES = {
    "gpu": "Display",
    "storage": "SCSIAdapter",
    "network": "Net",
    "usb": "USB",
}


def list_devices(category: str):
    """Returns [(friendly_name, instance_id), ...] for a device category."""
    cls = CATEGORY_CLASSES.get(category, category)
    ps = (
        f"Get-PnpDevice -Class '{cls}' -Status OK | "
        f"Select-Object FriendlyName, InstanceId | ConvertTo-Csv -NoTypeInformation"
    )
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                          capture_output=True, text=True)
    rows = []
    for line in out.stdout.splitlines()[1:]:
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) == 2:
            rows.append((parts[0], parts[1].strip('"')))
    return rows


def get_msi_state(instance_id: str):
    path = (r"SYSTEM\CurrentControlSet\Enum\%s\Device Parameters"
            r"\Interrupt Management\MessageSignaledInterruptProperties" % instance_id)
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
            val, _ = winreg.QueryValueEx(key, "MSISupported")
            return bool(val)
    except FileNotFoundError:
        return None  # device doesn't expose MSI properties at all


def set_msi_state(instance_id: str, enabled: bool):
    path = (r"SYSTEM\CurrentControlSet\Enum\%s\Device Parameters"
            r"\Interrupt Management\MessageSignaledInterruptProperties" % instance_id)
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
    winreg.SetValueEx(key, "MSISupported", 0, winreg.REG_DWORD, 1 if enabled else 0)
    winreg.CloseKey(key)
