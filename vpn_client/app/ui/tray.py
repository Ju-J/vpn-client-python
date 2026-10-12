from __future__ import annotations

from typing import Optional

from vpn_client.app.controllers.vpn_manager import VPNManager
from vpn_client.app.logging.app_logger import AppLogger


class TrayIcon:
    """Tray abstraction; implement with PySide6 QSystemTrayIcon or a desktop-specific tray library."""

    def __init__(self, manager: Optional[VPNManager] = None, logger: Optional[AppLogger] = None) -> None:
        self.manager = manager or VPNManager()
        self.logger = logger or AppLogger("vpn_client.tray")
        self.visible = True

    def show(self) -> None:
        self.visible = True
        self.logger.info("tray_show")

    def hide(self) -> None:
        self.visible = False
        self.logger.info("tray_hide")

    def set_tooltip(self, text: str) -> None:
        self.logger.info("tray_tooltip", tooltip=text)
