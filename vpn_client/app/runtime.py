from __future__ import annotations

from typing import Optional

from vpn_client.app.controllers.connection_state import ConnectionStateMachine
from vpn_client.app.controllers.reconnect_manager import ReconnectManager
from vpn_client.app.controllers.vpn_manager import VPNManager
from vpn_client.app.logging.app_logger import AppLogger


class AppRuntime:
    """Thin runtime coordinator tying together connection state, reconnect logic, and monitor checks."""

    def __init__(
        self,
        state_machine: Optional[ConnectionStateMachine] = None,
        manager: Optional[VPNManager] = None,
        logger: Optional[AppLogger] = None,
    ) -> None:
        self.manager = manager or VPNManager(logger=logger)
        self.state_machine = state_machine or self.manager.state_machine
        self.logger = logger or AppLogger("vpn_client.runtime")
        self.reconnect_manager = ReconnectManager(logger=self.logger)

    def connect(self, profile_id: str, action=None) -> bool:
        if action is None:
            action = lambda: self.manager.connect(profile_id)

        self.logger.info("runtime_connect_requested", profile_id=profile_id)
        ok = self.reconnect_manager.retry(action, label=f"connection:{profile_id}")
        if ok:
            self.state_machine.transition(self.manager.status, message="runtime_connected")
        return ok

    def disconnect(self) -> bool:
        self.logger.info("runtime_disconnect_requested")
        ok = self.manager.disconnect()
        if ok:
            self.state_machine.transition(self.manager.status, message="runtime_disconnected")
        return ok

    def health_check(self) -> bool:
        return self.manager.health_check()

    def status(self):
        return self.manager.status
