"""Small factory shared by every data/*_tweaks.py file so each tweak definition is one line."""
from core import registry_engine as reg
from core import service_engine as svc


def reg_toggle(tid, path, name, on_val, off_val, rtype="REG_DWORD"):
    def apply_():
        reg.write_value(path, name, on_val, rtype, tid)

    def revert_():
        reg.restore_tweak(tid)

    def check_():
        v, _ = reg.read_value(path, name)
        return v == on_val

    return apply_, revert_, check_


def service_toggle(service_name):
    tid = f"svc_{service_name}"

    def apply_():
        svc.set_start_type(service_name, "disabled", tid)

    def revert_():
        svc.restore_service(service_name)

    def check_():
        return svc.get_start_type(service_name) == "disabled"

    return apply_, revert_, check_
