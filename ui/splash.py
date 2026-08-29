"""
Splash screen shown before anything else.
------------------------------------------
Step 1: language picker (فارسی / English) — sets core.i18n.LANG.
Step 2: a short loading animation while the (slightly heavy — 15 tabs,
        100 games, icon assets) main window is constructed, so the user
        never sees a frozen/blank window on startup.
"""
import os
import customtkinter as ctk
from PIL import Image
from core import i18n
from core import theme


class SplashScreen(ctk.CTk):
    def __init__(self, on_ready):
        super().__init__()
        self.on_ready = on_ready
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(theme.THEME_JSON)

        self.title("Gaming Optimizer")
        self.geometry("480x320")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        self._build_language_step()

    # ---------- step 1: language ----------

    def _build_language_step(self):
        for w in self.winfo_children():
            w.destroy()

        logo_img = Image.open(os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png"))
        logo_ctk = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(80, 80))
        ctk.CTkLabel(self, text="", image=logo_ctk).pack(pady=(20, 6))
        ctk.CTkLabel(self, text="Gaming Optimizer", font=("Segoe UI", 20, "bold"), text_color=theme.RED).pack()
        ctk.CTkLabel(self, text="زبان را انتخاب کنید  /  Choose your language",
                     text_color=theme.TEXT_MUTED, font=("Segoe UI", 12)).pack(pady=(6, 24))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack()
        ctk.CTkButton(row, text="فارسی", width=160, height=44, font=("Segoe UI", 14),
                      command=lambda: self._choose_language("fa")).pack(side="right", padx=8)
        ctk.CTkButton(row, text="English", width=160, height=44, font=("Segoe UI", 14),
                      command=lambda: self._choose_language("en")).pack(side="left", padx=8)

    def _choose_language(self, lang):
        i18n.set_lang(lang)
        self._build_loading_step()

    # ---------- step 2: loading ----------

    def _build_loading_step(self):
        for w in self.winfo_children():
            w.destroy()

        logo_img2 = Image.open(os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png"))
        logo_ctk2 = ctk.CTkImage(light_image=logo_img2, dark_image=logo_img2, size=(60, 60))
        ctk.CTkLabel(self, text="", image=logo_ctk2).pack(pady=(30, 10))
        self.status_label = ctk.CTkLabel(self, text=i18n.t("splash_loading"), font=("Segoe UI", 13))
        self.status_label.pack(pady=(0, 14))

        self.bar = ctk.CTkProgressBar(self, width=340, mode="indeterminate")
        self.bar.pack(pady=6)
        self.bar.start()

        # give the UI a moment to paint the loading screen before the (synchronous,
        # somewhat heavy) main-window construction blocks the thread
        self.after(150, self._finish)

    def _finish(self):
        self.bar.stop()
        self.destroy()
        self.on_ready()
