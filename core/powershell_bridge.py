"""Small wrapper so tabs don't repeat subprocess boilerplate for BCD / powercfg / netsh etc."""
import subprocess


def run(cmd: str, shell="powershell") -> subprocess.CompletedProcess:
    if shell == "powershell":
        return subprocess.run(["powershell", "-NoProfile", "-Command", cmd],
                               capture_output=True, text=True)
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def run_bcdedit(args: str) -> subprocess.CompletedProcess:
    return subprocess.run(f"bcdedit {args}", shell=True, capture_output=True, text=True)


def run_powercfg(args: str) -> subprocess.CompletedProcess:
    return subprocess.run(f"powercfg {args}", shell=True, capture_output=True, text=True)


def run_netsh(args: str) -> subprocess.CompletedProcess:
    return subprocess.run(f"netsh {args}", shell=True, capture_output=True, text=True)
