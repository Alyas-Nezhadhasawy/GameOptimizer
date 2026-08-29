import customtkinter as ctk
from core import msi_mode_engine as msi
from core import i18n
from core import theme

CATEGORIES = [("gpu", i18n.t("cat_gpu")), ("storage", i18n.t("cat_storage")),
              ("network", i18n.t("cat_network")), ("usb", i18n.t("cat_usb"))]


class MSIModeTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text=i18n.t("msi_title"), font=("Segoe UI", 20, "bold")
                     ).pack(anchor="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(self, text=i18n.t("msi_subtitle"),
                     text_color=theme.TEXT_MUTED, font=("Segoe UI", 12)).pack(anchor="w", padx=20)

        self.cat_var = ctk.StringVar(value="gpu")
        seg = ctk.CTkSegmentedButton(
            self, values=[c[0] for c in CATEGORIES], variable=self.cat_var,
            command=lambda _: self.refresh())
        seg.pack(padx=20, pady=12, fill="x")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=12, pady=4)

        ctk.CTkButton(self, text=i18n.t("msi_rescan"), command=self.refresh
                      ).pack(padx=20, pady=(0, 12), anchor="w")
        self.refresh()

    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        try:
            devices = msi.list_devices(self.cat_var.get())
        except Exception as e:
            ctk.CTkLabel(self.scroll, text=f"خطا در خواندن دستگاه‌ها: {e}").pack(pady=20)
            return
        if not devices:
            ctk.CTkLabel(self.scroll, text=i18n.t("msi_none"),
                         text_color=theme.TEXT_MUTED).pack(pady=20)
            return
        for name, instance_id in devices:
            self._device_row(name, instance_id)

    def _device_row(self, name, instance_id):
        row = ctk.CTkFrame(self.scroll, corner_radius=10)
        row.pack(fill="x", pady=5, padx=6)
        ctk.CTkLabel(row, text=name, font=("Segoe UI", 13, "bold")).pack(
            side="right", padx=12, pady=10)

        state = msi.get_msi_state(instance_id)
        var = ctk.BooleanVar(value=bool(state))
        switch = ctk.CTkSwitch(row, text="MSI فعال", variable=var,
                                command=lambda: self._toggle(instance_id, var))
        switch.pack(side="left", padx=12)
        if state is None:
            switch.configure(state="disabled")
            ctk.CTkLabel(row, text=i18n.t("msi_no_param"),
                         text_color=theme.TEXT_MUTED, font=("Segoe UI", 10)).pack(side="left")

    def _toggle(self, instance_id, var):
        try:
            msi.set_msi_state(instance_id, var.get())
        except Exception as e:
            var.set(not var.get())
            print("MSI toggle error:", e)
