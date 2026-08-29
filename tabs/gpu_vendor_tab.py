import subprocess
import threading
import customtkinter as ctk
from core import i18n
from data.gpu_vendor_guide import GUIDES, detect_vendor_hint
from core import theme

VENDOR_LABELS = {"nvidia": "NVIDIA", "amd": "AMD", "intel": "Intel"}


class GPUVendorTab(ctk.CTkFrame):
    """
    Customization menu: pick your GPU brand (auto-detected as a starting
    point, but always user-overridable) and get an accurate, vendor-specific
    settings guide instead of one generic list that only really applies to
    one brand.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        ctk.CTkLabel(self, text=i18n.t("gpu_vendor_title"), font=("Segoe UI", 20, "bold")
                     ).pack(anchor="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(self, text=i18n.t("gpu_vendor_subtitle"), text_color=theme.TEXT_MUTED,
                     font=("Segoe UI", 12)).pack(anchor="w", padx=20)

        self.vendor_var = ctk.StringVar(value="nvidia")
        self.selector = ctk.CTkSegmentedButton(
            self, values=["nvidia", "amd", "intel"], variable=self.vendor_var,
            command=lambda _: self.render())
        self.selector.pack(padx=20, pady=14, fill="x")

        self.content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=12, pady=4)

        threading.Thread(target=self._auto_detect, daemon=True).start()
        self.render()

    def _auto_detect(self):
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"],
                capture_output=True, text=True)
            name = out.stdout.strip().splitlines()[0] if out.stdout.strip() else ""
        except Exception:
            name = ""
        vendor = detect_vendor_hint(name)
        self.after(0, lambda: (self.vendor_var.set(vendor), self.render()))

    def render(self):
        for w in self.content.winfo_children():
            w.destroy()

        vendor = self.vendor_var.get()
        guide = GUIDES[vendor]
        lang = "en" if i18n.LANG == "en" else "fa"
        text = guide[lang]

        card = ctk.CTkFrame(self.content, corner_radius=12)
        card.pack(fill="x", padx=6, pady=8)
        ctk.CTkLabel(card, text=text["title"], font=("Segoe UI", 16, "bold")
                     ).pack(anchor="e", padx=16, pady=(14, 4))
        ctk.CTkLabel(card, text=text["launch_hint"], text_color=theme.TEXT_MUTED,
                     font=("Segoe UI", 11), wraplength=560, justify="right"
                     ).pack(anchor="e", padx=16)

        for i, step in enumerate(text["steps"], start=1):
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4, anchor="e")
            ctk.CTkLabel(row, text=f"{i}.", text_color=theme.RED,
                         font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 8))
            ctk.CTkLabel(row, text=step, font=("Segoe UI", 12), wraplength=520,
                         justify="right").pack(side="left")

        ctk.CTkButton(card, text=i18n.t("gpu_vendor_open_panel"),
                      command=lambda: self._launch(guide["launch_cmd"])
                      ).pack(anchor="e", padx=16, pady=(10, 16))

    def _launch(self, candidates):
        def worker():
            for exe in candidates:
                try:
                    subprocess.Popen(exe)
                    return
                except Exception:
                    continue
        threading.Thread(target=worker, daemon=True).start()
