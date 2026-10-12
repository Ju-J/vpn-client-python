from __future__ import annotations

from typing import Optional

from vpn_client.app.controllers.connection_state import ConnectionState
from vpn_client.app.controllers.vpn_manager import VPNManager
from vpn_client.app.logging.app_logger import AppLogger


class MainWindow:
    """Minimal shell for app UI; this is a placeholder for a PySide6 or Tkinter implementation."""

    def __init__(self, manager: Optional[VPNManager] = None, logger: Optional[AppLogger] = None) -> None:
        self.manager = manager or VPNManager()
        self.logger = logger or AppLogger("vpn_client.ui")

    def render_status(self) -> str:
        state = self.manager.status.value if self.manager.status else ConnectionState.DISCONNECTED.value
        return f"VPN client status: {state}"

    def show(self) -> None:
        self.logger.info("ui_window_shown", status=self.render_status())

    def refresh(self) -> None:
        self.logger.info("ui_refreshed", status=self.render_status())
