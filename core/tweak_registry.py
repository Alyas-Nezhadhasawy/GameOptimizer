"""Central registry of every Tweak object defined across data/*.py, keyed by id.
Used by the Games tab so 'apply recommended tweaks for this game' can reuse
the exact same apply()/revert()/is_applied() functions already built for the
regular tabs, instead of duplicating logic.
"""
from data import (registry_bcd_tweaks, windows_settings_tweaks, control_panel_tweaks,
                   network_tweaks, ram_tweaks, gpu_tweaks)

_cache = None


def build_registry():
    global _cache
    if _cache is not None:
        return _cache
    all_tweaks = {}
    builders = [registry_bcd_tweaks.build, windows_settings_tweaks.build, control_panel_tweaks.build,
                network_tweaks.build, ram_tweaks.build, gpu_tweaks.build]
    for builder in builders:
        for tweak in builder():
            all_tweaks[tweak.id] = tweak

    # power_plan tweaks live inside the tab module itself (they were built there originally)
    try:
        from tabs.power_plan_tab import _build_tweaks as build_power_tweaks
        for tweak in build_power_tweaks():
            all_tweaks[tweak.id] = tweak
    except Exception:
        pass

    _cache = all_tweaks
    return all_tweaks
