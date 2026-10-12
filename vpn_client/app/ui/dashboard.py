from __future__ import annotations

from typing import Optional

from vpn_client.app.controllers.connection_state import ConnectionState
from vpn_client.app.controllers.vpn_manager import VPNManager
from vpn_client.app.logging.app_logger import AppLogger
from vpn_client.app.runtime import AppRuntime


class Dashboard:
    """Minimal dashboard state view for the app shell."""

    def __init__(self, runtime: Optional[AppRuntime] = None, manager: Optional[VPNManager] = None, logger: Optional[AppLogger] = None) -> None:
        self.runtime = runtime or AppRuntime()
        self.manager = manager or VPNManager(logger=logger)
        self.logger = logger or AppLogger("vpn_client.dashboard")

    def status_text(self) -> str:
        state = self.manager.status.value if self.manager.status else ConnectionState.DISCONNECTED.value
        return f"Status: {state}"

    def refresh(self) -> None:
        self.logger.info("dashboard_refresh", status=self.status_text())

