from __future__ import annotations

import dataclasses
import enum
from typing import Any, Dict, Optional


class ConnectionState(enum.Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTING = "disconnecting"
    RECONNECTING = "reconnecting"
    ERROR = "error"


@dataclasses.dataclass
class ConnectionEvent:
    state: ConnectionState
    protocol: Optional[str] = None
    message: str = ""
    details: Optional[Dict[str, Any]] = None


class ConnectionStateMachine:
    def __init__(self) -> None:
        self.state = ConnectionState.DISCONNECTED
        self.last_event: Optional[ConnectionEvent] = None

    def transition(self, new_state: ConnectionState, protocol: Optional[str] = None, message: str = "", details: Optional[Dict[str, Any]] = None) -> None:
        self.state = new_state
        self.last_event = ConnectionEvent(
            state=new_state,
            protocol=protocol,
            message=message,
            details=details or {},
        )

    def reset(self) -> None:
        self.transition(ConnectionState.DISCONNECTED, message="reset")
