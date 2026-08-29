"""
Central "black & red" palette.
-------------------------------
Two things live here:

1. THEME_JSON — path passed to ctk.set_default_color_theme(...). This is
   what actually re-colors every widget that does NOT set its own
   fg_color/hover_color explicitly (plain CTkButton, CTkSwitch progress
   color, CTkProgressBar, scrollbars, the splash-screen language buttons,
   dialog OK buttons, ...). Before this file existed the app called
   ctk.set_default_color_theme("dark-blue"), so every one of those
   widgets rendered blue no matter what the rest of the UI looked like.

2. Named color constants — for the handful of places that set an explicit
   fg_color/text_color (sidebar, cards, risk labels). Importing from here
   instead of repeating hex literals means the whole app can be re-themed
   by editing exactly one file.
"""
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
THEME_JSON = os.path.join(ASSETS_DIR, "theme", "black_red.json")

# ---- backgrounds (darkest -> lightest) ----
BG_ROOT = "#0b0d10"
BG_SIDEBAR = "#111318"
BG_CONTENT = "#15171c"
BG_CARD = "#1a1d24"
BG_HOVER = "#1d2230"
BORDER = "#262b33"

# ---- accent (flat "red / pomegranate" pair) ----
RED = "#e74c3c"
RED_DARK = "#c0392b"
RED_DARKER = "#922b21"

# ---- text ----
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#9aa0a6"
TEXT_ON_RED = "#0b0d10"

# ---- status ----
SUCCESS = "#2ecc71"
WARNING = "#f1c40f"
DANGER = RED
