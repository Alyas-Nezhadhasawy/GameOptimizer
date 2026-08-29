"""
Every checkbox/switch in the whole app is one Tweak object.
Tabs just build a list[Tweak] and hand it to GenericTweakTab to render.
"""
from dataclasses import dataclass, field
from typing import Callable, Optional

RISK_SAFE = "safe"        # fully reversible, no downside
RISK_MEDIUM = "medium"    # reversible, but changes real behavior (e.g. disables a service)
RISK_HIGH = "high"        # security/stability trade-off (e.g. disables Core Isolation)


@dataclass
class Tweak:
    id: str
    name: str                       # Persian display name
    description: str                # 1-2 line Persian explanation
    apply: Callable[[], None]
    revert: Callable[[], None]
    is_applied: Callable[[], bool]
    risk: str = RISK_SAFE
    requires_admin: bool = True
    category: str = ""
