import io
import os
import threading
import urllib.request
import customtkinter as ctk
from PIL import Image

from core import i18n
from core.tweak_registry import build_registry
from data.games_data import GAMES
from data.game_settings_templates import TEMPLATES, GENRE_TWEAK_IDS
from ui.progress_dialog import ProgressDialog
from core import theme

# Local poster directory (bundled with app — works offline)
POSTER_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "posters")

# Map non-Steam game names to custom poster filenames
CUSTOM_POSTERS = {
    "Valorant": "valorant",
    "Fortnite": "fortnite",
    "League of Legends": "lol",
    "Genshin Impact": "genshin",
    "World of Warcraft": "wow",
    "Escape from Tarkov": "tarkov",
    "Minecraft": "minecraft",
}


def _get_poster_path(appid, name):
    """Returns the local poster path for a game, whether Steam or custom."""
    if appid is not None:
        return os.path.join(POSTER_DIR, f"{appid}.jpg")
    custom = CUSTOM_POSTERS.get(name)
    if custom:
        return os.path.join(POSTER_DIR, f"{custom}.jpg")
    return None


CARD_W, CARD_H = 230, 108


class GamesTab(ctk.CTkFrame):
    """
    Grid of popular games. Posters are bundled locally in assets/posters/
    so everything works offline — no internet required. Click a card to see
    genre-based recommended settings and optionally apply the relevant
    OS-level tweaks with one button.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._image_cache = {}
        self._placeholder = self._make_placeholder()

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 4))
        ctk.CTkLabel(header, text=i18n.t("games_title"), font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(header, text=i18n.t("games_subtitle"), text_color=theme.TEXT_MUTED,
                     font=("Segoe UI", 12)).pack(anchor="w")

        self.search_var = ctk.StringVar()
        search = ctk.CTkEntry(self, placeholder_text=i18n.t("games_search"), textvariable=self.search_var)
        search.pack(fill="x", padx=20, pady=8)
        self.search_var.trace_add("write", lambda *_: self._rebuild_grid())

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=12, pady=4)

        self._rebuild_grid()

    def _make_placeholder(self):
        img = Image.new("RGBA", (CARD_W, CARD_H), (26, 29, 36, 255))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(CARD_W, CARD_H))

    def _rebuild_grid(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        query = self.search_var.get().strip().lower()
        games = [g for g in GAMES if query in g[0].lower()] if query else GAMES

        cols = 3
        for i, (name, appid, genre) in enumerate(games):
            r, c = divmod(i, cols)
            card = self._build_card(self.scroll, name, appid, genre)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
        for c in range(cols):
            self.scroll.grid_columnconfigure(c, weight=1)

    def _build_card(self, parent, name, appid, genre):
        card = ctk.CTkFrame(parent, corner_radius=10, width=CARD_W)
        img_label = ctk.CTkLabel(card, text="", image=self._placeholder)
        img_label.pack(padx=6, pady=(6, 4))
        ctk.CTkLabel(card, text=name, font=("Segoe UI", 12, "bold"),
                     wraplength=CARD_W - 10).pack(padx=6, pady=(0, 8))

        card.bind("<Button-1>", lambda e: self._open_details(name, appid, genre))
        img_label.bind("<Button-1>", lambda e: self._open_details(name, appid, genre))

        threading.Thread(target=self._load_poster, args=(appid, img_label, name), daemon=True).start()
        return card

    def _load_poster(self, appid, img_label, name=""):
        cache_key = appid if appid is not None else name
        if cache_key in self._image_cache:
            ctk_img = self._image_cache[cache_key]
        else:
            try:
                path = _get_poster_path(appid, name)
                if path and os.path.exists(path):
                    pil_img = Image.open(path).convert("RGBA").resize((CARD_W, CARD_H))
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(CARD_W, CARD_H))
                    self._image_cache[cache_key] = ctk_img
                else:
                    return  # keep placeholder
            except Exception:
                return  # keep placeholder
        self.after(0, lambda: img_label.configure(image=ctk_img))

    def _open_details(self, name, appid, genre):
        dialog = ctk.CTkToplevel(self)
        dialog.title(name)
        dialog.geometry("520x560")
        dialog.attributes("-topmost", True)
        dialog.grab_set()

        img_label = ctk.CTkLabel(dialog, text="", image=self._image_cache.get(appid, self._placeholder))
        img_label.pack(pady=(16, 8))
        if (appid and appid not in self._image_cache) or (not appid and name not in self._image_cache):
            threading.Thread(target=self._load_poster, args=(appid, img_label, name), daemon=True).start()

        ctk.CTkLabel(dialog, text=f"{i18n.t('games_settings_for')} {name}",
                     font=("Segoe UI", 15, "bold")).pack(pady=(0, 8), padx=16)

        scroll = ctk.CTkScrollableFrame(dialog, fg_color="transparent", height=280)
        scroll.pack(fill="both", expand=True, padx=16)
        lang = "en" if i18n.LANG == "en" else "fa"
        for line in TEMPLATES.get(genre, {}).get(lang, []):
            ctk.CTkLabel(scroll, text=f"• {line}", wraplength=460, justify="right",
                         font=("Segoe UI", 12), anchor="e").pack(fill="x", pady=3, anchor="e")

        ctk.CTkButton(dialog, text=i18n.t("games_apply_recommended"),
                      command=lambda: self._apply_recommended(genre, dialog)
                      ).pack(pady=(8, 6), padx=16, fill="x")
        ctk.CTkButton(dialog, text=i18n.t("ok"), fg_color="#555", hover_color="#444",
                      command=dialog.destroy).pack(pady=(0, 16), padx=16, fill="x")

    def _apply_recommended(self, genre, parent_dialog):
        ids = GENRE_TWEAK_IDS.get(genre, [])
        registry = build_registry()
        tweaks = [registry[tid] for tid in ids if tid in registry]
        if not tweaks:
            return
        dialog = ProgressDialog(parent_dialog, title=i18n.t("games_apply_recommended") + "...")
        total = len(tweaks)

        def worker():
            failed = []
            for i, tweak in enumerate(tweaks, start=1):
                name = i18n.tweak_name(tweak)
                dialog.update_progress((i - 1) / total, f"{name} ({i}/{total})")
                try:
                    tweak.apply()
                except Exception as e:
                    failed.append((name, str(e)))
                dialog.update_progress(i / total, f"{name} ({i}/{total})")
            msg = f"✅ {total - len(failed)}/{total}" + (f" · ❌ {len(failed)}" if failed else "")
            dialog.finish(msg)

        threading.Thread(target=worker, daemon=True).start()
