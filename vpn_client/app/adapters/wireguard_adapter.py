from __future__ import annotations

from typing import Any, Dict

from vpn_client.app.adapters.base_adapter import BaseAdapter
from vpn_client.app.logging.app_logger import AppLogger
from vpn_client.app.models.profile import VPNProfile
from vpn_client.app.system.protocol_commands import build_connect_command, build_disconnect_command, build_health_check_command


class WireGuardAdapter(BaseAdapter):
    def __init__(self, profile: VPNProfile, logger: AppLogger) -> None:
        super().__init__(profile, logger)

    def connect(self) -> bool:
        self.assert_ready()
        command = build_connect_command(self.profile)
        validation_errors = self.validate_runtime(command)
        if validation_errors:
            raise RuntimeError("; ".join(validation_errors))
        self.logger.info("wireguard_connect_attempt", profile_id=self.profile.id, command=command)
        self.connected = True
        return True

    def disconnect(self) -> bool:
        command = build_disconnect_command(self.profile)
        validation_errors = self.validate_runtime(command)
        if validation_errors:
            raise RuntimeError("; ".join(validation_errors))
        self.logger.info("wireguard_disconnect_attempt", profile_id=self.profile.id, command=command)
        self.connected = False
        return True

    def health_check(self) -> bool:
        if not self.connected:
            return False
        errors = self.validator.validate_command(build_health_check_command(self.profile))
        return not errors

    def get_status(self) -> Dict[str, Any]:
        return {"protocol": "wireguard", "connected": self.connected, "profile_id": self.profile.id}
