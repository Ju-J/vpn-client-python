from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Sequence

from vpn_client.app.system.command_validation import CommandValidator
from vpn_client.app.system.protocol_commands import build_connect_command, build_disconnect_command, build_health_check_command


class BaseAdapter(ABC):
    def __init__(self, profile: Any, logger: Any) -> None:
        self.profile = profile
        self.logger = logger
        self.connected = False
        self.validator = CommandValidator()

    def assert_ready(self) -> None:
        errors = self.validator.validate_profile(self.profile)
        if errors:
            raise RuntimeError("; ".join(errors))

    def validate_runtime(self, command: Optional[Sequence[str]] = None) -> list[str]:
        if command is None:
            command = build_connect_command(self.profile)
        return self.validator.validate_command(command)

    def disconnect_command(self) -> list[str]:
        return build_disconnect_command(self.profile)

    def health_command(self) -> list[str]:
        return build_health_check_command(self.profile)

    @abstractmethod
    def connect(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        raise NotImplementedError

    def update_state(self, state: str, message: str = "", **details: Any) -> None:
        self.logger.info(message or state, state=state, **details)
