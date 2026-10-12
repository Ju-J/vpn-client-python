from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from vpn_client.app.adapters.base_adapter import BaseAdapter
from vpn_client.app.adapters.openvpn_adapter import OpenVPNAdapter
from vpn_client.app.adapters.socks5_adapter import SOCKS5Adapter
from vpn_client.app.adapters.ssh_adapter import SSHAdapter
from vpn_client.app.adapters.sstp_adapter import SSTPAdapter
from vpn_client.app.adapters.wireguard_adapter import WireGuardAdapter
from vpn_client.app.controllers.connection_state import ConnectionState, ConnectionStateMachine
from vpn_client.app.logging.app_logger import AppLogger
from vpn_client.app.models.profile import ProtocolType, VPNProfile


class VPNManager:
    def __init__(self, profiles: Optional[List[VPNProfile]] = None, logger: Optional[AppLogger] = None) -> None:
        self.logger = logger or AppLogger("vpn_client")
        self.state_machine = ConnectionStateMachine()
        self.profiles: Dict[str, VPNProfile] = {}
        self.active_adapter: Optional[BaseAdapter] = None

        if profiles:
            for profile in profiles:
                self.profiles[profile.id] = profile

    def add_profile(self, profile: VPNProfile) -> None:
        self.profiles[profile.id] = profile

    def get_profile(self, profile_id: str) -> Optional[VPNProfile]:
        return self.profiles.get(profile_id)

    def list_profiles(self) -> List[VPNProfile]:
        return list(self.profiles.values())

    def create_adapter(self, profile: VPNProfile) -> BaseAdapter:
        if profile.protocol == ProtocolType.WIREGUARD:
            return WireGuardAdapter(profile, self.logger)
        if profile.protocol == ProtocolType.OPENVPN:
            return OpenVPNAdapter(profile, self.logger)
        if profile.protocol == ProtocolType.SSH:
            return SSHAdapter(profile, self.logger)
        if profile.protocol == ProtocolType.SOCKS5:
            return SOCKS5Adapter(profile, self.logger)
        if profile.protocol == ProtocolType.SSTP:
            return SSTPAdapter(profile, self.logger)
        raise ValueError(f"Unsupported protocol: {profile.protocol}")

    def connect(self, profile_id: str) -> bool:
        profile = self.get_profile(profile_id)
        if profile is None:
            self.logger.error("profile_not_found", profile_id=profile_id)
            self.state_machine.transition(ConnectionState.ERROR, protocol=None, message="Profile not found")
            return False

        self.logger.info("attempting_connection", profile_id=profile_id, protocol=profile.protocol.value)
        self.state_machine.transition(ConnectionState.CONNECTING, protocol=profile.protocol.value, message="Connecting")

        adapter = self.create_adapter(profile)
        self.active_adapter = adapter

        try:
            success = adapter.connect()
            if success:
                self.state_machine.transition(ConnectionState.CONNECTED, protocol=profile.protocol.value, message="Connected")
                return True
            self.state_machine.transition(ConnectionState.ERROR, protocol=profile.protocol.value, message="Connection attempt failed")
            return False
        except Exception as exc:  # pragma: no cover
            self.logger.error("connection_exception", profile_id=profile_id, error=str(exc))
            self.state_machine.transition(ConnectionState.ERROR, protocol=profile.protocol.value, message=str(exc))
            return False

    def disconnect(self) -> bool:
        if self.active_adapter is None:
            self.state_machine.transition(ConnectionState.DISCONNECTED, message="No active adapter")
            return True

        self.state_machine.transition(ConnectionState.DISCONNECTING, protocol=self.active_adapter.profile.protocol.value, message="Disconnecting")
        try:
            success = self.active_adapter.disconnect()
            if success:
                self.state_machine.transition(ConnectionState.DISCONNECTED, protocol=self.active_adapter.profile.protocol.value, message="Disconnected")
                self.active_adapter = None
                return True
            self.state_machine.transition(ConnectionState.ERROR, protocol=self.active_adapter.profile.protocol.value, message="Disconnect failed")
            return False
        except Exception as exc:  # pragma: no cover
            self.logger.error("disconnect_exception", error=str(exc))
            self.state_machine.transition(ConnectionState.ERROR, protocol=self.active_adapter.profile.protocol.value, message=str(exc))
            return False

    def save_profiles(self, file_path: str | Path) -> None:
        payload = {
            "profiles": [profile.to_dict() for profile in self.list_profiles()]
        }
        Path(file_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_profiles(self, file_path: str | Path) -> List[VPNProfile]:
        path = Path(file_path)
        if not path.exists():
            return []

        data = json.loads(path.read_text(encoding="utf-8"))
        profiles = [VPNProfile.from_dict(item) for item in data.get("profiles", [])]
        for profile in profiles:
            self.profiles[profile.id] = profile
        return profiles

    def health_check(self) -> bool:
        if self.active_adapter is None:
            return False
        ok = self.active_adapter.health_check()
        if ok:
            self.state_machine.transition(ConnectionState.CONNECTED, protocol=self.active_adapter.profile.protocol.value, message="Healthy")
        else:
            self.state_machine.transition(ConnectionState.ERROR, protocol=self.active_adapter.profile.protocol.value, message="Health check failed")
        return ok

    @property
    def status(self) -> ConnectionState:
        return self.state_machine.state
