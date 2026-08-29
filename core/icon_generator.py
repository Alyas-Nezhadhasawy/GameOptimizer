"""
Generates a clean, consistent flat-icon set for the sidebar using Pillow.

We deliberately do NOT download screenshots of NVIDIA/AMD control panels,
Windows Settings, etc. from the internet: those are copyrighted UI assets
and bundling them in a distributed app is a real legal risk. Instead we
draw simple single-color glyphs that match a dark gaming theme -- run this
once (`python -m core.icon_generator`) to (re)generate assets/icons/*.png.
"""
import os
from PIL import Image, ImageDraw

ICON_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "icons")
SIZE = 64
ACCENT = (231, 76, 60, 255)   # red accent, matches UI theme
BG = (0, 0, 0, 0)


def _canvas():
    return Image.new("RGBA", (SIZE, SIZE), BG)


def _save(img, name):
    os.makedirs(ICON_DIR, exist_ok=True)
    img.save(os.path.join(ICON_DIR, f"{name}.png"))


def icon_rocket(): 
    img = _canvas(); d = ImageDraw.Draw(img)
    d.polygon([(32, 6), (46, 42), (32, 34), (18, 42)], fill=ACCENT)
    d.ellipse((26, 20, 38, 32), fill=BG, outline=ACCENT, width=3)
    _save(img, "start")


def icon_registry():
    img = _canvas(); d = ImageDraw.Draw(img)
    for i in range(3):
        d.rectangle((10, 12 + i * 16, 54, 24 + i * 16), outline=ACCENT, width=3)
    _save(img, "registry")


def icon_gear(name):
    img = _canvas(); d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), outline=ACCENT, width=4)
    d.ellipse((26, 26, 38, 38), fill=ACCENT)
    _save(img, name)


def icon_power():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.arc((14, 14, 50, 50), start=40, end=320, fill=ACCENT, width=5)
    d.line((32, 8, 32, 30), fill=ACCENT, width=5)
    _save(img, "power")


def icon_gpu():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 20, 56, 44), radius=6, outline=ACCENT, width=4)
    for x in range(16, 50, 8):
        d.line((x, 44, x, 52), fill=ACCENT, width=3)
    _save(img, "gpu")


def icon_broom():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.polygon([(40, 6), (54, 20), (24, 50), (18, 44)], fill=ACCENT)
    d.line((24, 50, 10, 58), fill=ACCENT, width=4)
    _save(img, "cleanup")


def icon_services():
    img = _canvas(); d = ImageDraw.Draw(img)
    for i, y in enumerate((16, 30, 44)):
        d.rectangle((10, y, 40, y + 8), fill=ACCENT if i != 1 else BG,
                     outline=ACCENT, width=2)
    _save(img, "services")


def icon_chip():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.rectangle((18, 18, 46, 46), outline=ACCENT, width=4)
    for x in (24, 32, 40):
        d.line((x, 6, x, 18), fill=ACCENT, width=3)
        d.line((x, 46, x, 58), fill=ACCENT, width=3)
    _save(img, "msi")


def icon_network():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.arc((8, 20, 56, 68), start=200, end=340, fill=ACCENT, width=4)
    d.arc((16, 28, 48, 60), start=200, end=340, fill=ACCENT, width=4)
    d.ellipse((28, 42, 36, 50), fill=ACCENT)
    _save(img, "network")


def icon_ram():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.rectangle((10, 20, 54, 40), outline=ACCENT, width=4)
    for x in range(16, 50, 6):
        d.line((x, 40, x, 48), fill=ACCENT, width=3)
    _save(img, "ram")


def icon_adobe():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.polygon([(20, 10), (44, 10), (58, 54), (44, 54)], outline=ACCENT, width=3)
    d.polygon([(32, 24), (40, 44), (24, 44)], fill=ACCENT)
    _save(img, "adobe")


def icon_priority():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.polygon([(32, 6), (40, 26), (60, 26), (44, 38), (50, 58),
               (32, 46), (14, 58), (20, 38), (4, 26), (24, 26)], outline=ACCENT, width=3)
    _save(img, "priority")


def icon_startup():
    img = _canvas(); d = ImageDraw.Draw(img)
    d.ellipse((14, 14, 50, 50), outline=ACCENT, width=4)
    d.polygon([(28, 22), (28, 42), (44, 32)], fill=ACCENT)
    _save(img, "startup")


def generate_all():
    icon_rocket()
    icon_registry()
    icon_gear("windows_settings")
    icon_gear("control_panel")
    icon_power()
    icon_gpu()
    icon_broom()
    icon_services()
    icon_chip()
    icon_gear("gpu_tweaks")
    icon_network()
    icon_ram()
    icon_adobe()
    icon_priority()
    icon_startup()
    print(f"Icons generated in {os.path.abspath(ICON_DIR)}")


if __name__ == "__main__":
    generate_all()
