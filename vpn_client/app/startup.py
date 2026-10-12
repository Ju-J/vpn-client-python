from __future__ import annotations

from vpn_client.app.controllers.vpn_manager import VPNManager
from vpn_client.app.logging.app_logger import AppLogger
from vpn_client.app.runtime import AppRuntime
from vpn_client.app.ui.dashboard import Dashboard
from vpn_client.app.ui.tray import TrayIcon


def wire_app_runtime() -> tuple[AppRuntime, VPNManager, Dashboard, TrayIcon, AppLogger]:
    logger = AppLogger("vpn_client.app")
    manager = VPNManager(logger=logger)
    runtime = AppRuntime(manager=manager, logger=logger)
    dashboard = Dashboard(manager=manager, logger=logger)
    tray = TrayIcon(manager=manager, logger=logger)
    return runtime, manager, dashboard, tray, logger


def app_main() -> None:
    runtime, manager, dashboard, tray, logger = wire_app_runtime()
    logger.info("app_runtime_wired")
    dashboard.refresh()
    tray.refresh()
    print(dashboard.status_text())


if __name__ == "__main__":
    app_main()
