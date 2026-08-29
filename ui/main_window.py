import customtkinter as ctk
from ui.sidebar import Sidebar

from tabs.start_tab import StartTab
from tabs.registry_bcd_tab import RegistryBCDTab
from tabs.windows_settings_tab import WindowsSettingsTab
from tabs.control_panel_tab import ControlPanelTab
from tabs.power_plan_tab import PowerPlanTab
from tabs.gpu_setting_tab import GPUSettingTab
from tabs.gpu_vendor_tab import GPUVendorTab
from tabs.games_tab import GamesTab
from tabs.cleanup_tab import CleanUpTab
from tabs.services_tab import ServicesTab
from tabs.msi_mode_tab import MSIModeTab
from tabs.gpu_tweaks_tab import GPUTweaksTab
from tabs.network_tab import NetworkTab
from tabs.ram_process_tab import RamProcessTab
from tabs.adobe_tab import AdobeTab
from tabs.game_priority_tab import GamePriorityTab
from tabs.startup_apps_tab import StartupAppsTab
from core import i18n
from core import theme

TAB_CLASSES = {
    "start": StartTab,
    "registry": RegistryBCDTab,
    "windows_settings": WindowsSettingsTab,
    "control_panel": ControlPanelTab,
    "power_plan": PowerPlanTab,
    "gpu_setting": GPUSettingTab,
    "gpu_vendor": GPUVendorTab,
    "games": GamesTab,
    "cleanup": CleanUpTab,
    "services": ServicesTab,
    "msi_mode": MSIModeTab,
    "gpu_tweaks": GPUTweaksTab,
    "network": NetworkTab,
    "ram": RamProcessTab,
    "adobe": AdobeTab,
    "priority": GamePriorityTab,
    "startup": StartupAppsTab,
}


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(i18n.t("window_title"))
        self.geometry("1050x680")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(theme.THEME_JSON)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, on_select=self.show_tab)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self, fg_color=theme.BG_CONTENT, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")

        self._current = None
        self._cache = {}
        self.show_tab("start")

    def show_tab(self, key):
        if self._current is not None:
            self._current.pack_forget()
        if key not in self._cache:
            self._cache[key] = TAB_CLASSES[key](self.content)
        self._current = self._cache[key]
        self._current.pack(fill="both", expand=True)


def run():
    app = MainWindow()
    app.mainloop()
