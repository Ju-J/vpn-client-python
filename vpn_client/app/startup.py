from __future__ import annotations

from pathlib import Path

from vpn_client.app.controllers.vpn_manager import VPNManager
from vpn_client.app.logging.app_logger import AppLogger
from vpn_client.app.runtime import AppRuntime
from vpn_client.app.ui.dashboard import Dashboard
from vpn_client.app.ui.main_window import MainWindow
from vpn_client.app.ui.tray import TrayIcon


def wire_app_runtime() -> tuple[AppRuntime, VPNManager, MainWindow, TrayIcon, Dashboard, AppLogger]:
    logger = AppLogger("vpn_client.app")
    runtime = AppRuntime(logger=logger)
    manager = VPNManager(logger=logger)
    window = MainWindow(manager=manager, logger=logger)
    tray = TrayIcon(manager=manager, logger=logger)
    dashboard = Dashboard(runtime=runtime, manager=manager, logger=logger)
    return runtime, manager, window, tray, dashboard, logger


def app_main() -> None:
    runtime, manager, window, tray, dashboard, logger = wire_app_runtime()
    logger.info("app_runtime_wired")
    window.show()
    tray.show()
    dashboard.refresh()
    print(window.render_status())


if __name__ == "__main__":
    app_main()
