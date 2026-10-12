from __future__ import annotations

from typing import Optional

from vpn_client.app.controllers.connection_state import ConnectionStateMachine
from vpn_client.app.controllers.reconnect_manager import ReconnectManager
from vpn_client.app.logging.app_logger import AppLogger


class AppRuntime:
    """Thin runtime coordinator tying together connection state, reconnect logic, and monitor checks."""

    def __init__(self, state_machine: Optional[ConnectionStateMachine] = None, logger: Optional[AppLogger] = None) -> None:
        self.state_machine = state_machine or ConnectionStateMachine()
        self.logger = logger or AppLogger("vpn_client.runtime")
        self.reconnect_manager = ReconnectManager(logger=self.logger)

    def connect_with_retry(self, action, label: str = "connection") -> bool:
        self.logger.info("runtime_connect_requested", label=label)
        return self.reconnect_manager.retry(action, label=label)

    def disconnect(self) -> bool:
        self.logger.info("runtime_disconnect_requested")
        return True
