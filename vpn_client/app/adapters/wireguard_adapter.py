from __future__ import annotations

from typing import Any, Dict

from vpn_client.app.adapters.base_adapter import BaseAdapter
from vpn_client.app.logging.app_logger import AppLogger
from vpn_client.app.models.profile import VPNProfile


class WireGuardAdapter(BaseAdapter):
    def __init__(self, profile: VPNProfile, logger: AppLogger) -> None:
        super().__init__(profile, logger)

    def connect(self) -> bool:
        self.logger.info("wireguard_connect_attempt", profile_id=self.profile.id)
        self.connected = True
        return True

    def disconnect(self) -> bool:
        self.logger.info("wireguard_disconnect_attempt", profile_id=self.profile.id)
        self.connected = False
        return True

    def health_check(self) -> bool:
        return self.connected

    def get_status(self) -> Dict[str, Any]:
        return {"protocol": "wireguard", "connected": self.connected, "profile_id": self.profile.id}

