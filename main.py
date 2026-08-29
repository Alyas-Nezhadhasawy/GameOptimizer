"""
Gaming Optimizer — entry point.
Run on Windows 10/11 as: python main.py   (or the packaged .exe)
Requires admin rights (auto-elevates via UAC prompt).
Shows a language-picker + loading splash before the main window opens.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import admin_utils


def launch_main_window():
    from ui.main_window import MainWindow
    app = MainWindow()
    app.mainloop()


def main():
    if sys.platform != "win32":
        print("This app only runs on Windows 10/11.")
        sys.exit(1)

    admin_utils.ensure_admin()  # relaunches elevated if needed, then exits this instance

    from ui.splash import SplashScreen
    splash = SplashScreen(on_ready=launch_main_window)
    splash.mainloop()


if __name__ == "__main__":
    main()
