from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any, Optional


class ProtocolType(str, Enum):
    WIREGUARD = "wireguard"
    OPENVPN = "openvpn"
    SSH = "ssh"
    SOCKS5 = "socks5"
    SSTP = "sstp"


@dataclasses.dataclass
class Endpoint:
    host: str
    port: int
    protocol: str = "udp"


@dataclasses.dataclass
class VPNProfile:
    id: str
    name: str
    protocol: ProtocolType
    endpoint: Optional[Endpoint] = None
    username: Optional[str] = None
    password: Optional[str] = None
    config_path: Optional[str] = None
    dns: Optional[str] = None
    mtu: Optional[int] = None
    allowed_ips: Optional[list[str]] = None
    auto_connect: bool = False
    reconnect_policy: str = "manual"
    kill_switch: bool = False
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "protocol": self.protocol.value,
            "endpoint": {
                "host": self.endpoint.host,
                "port": self.endpoint.port,
                "protocol": self.endpoint.protocol,
            } if self.endpoint else None,
            "username": self.username,
            "password": self.password,
            "config_path": self.config_path,
            "dns": self.dns,
            "mtu": self.mtu,
            "allowed_ips": self.allowed_ips,
            "auto_connect": self.auto_connect,
            "reconnect_policy": self.reconnect_policy,
            "kill_switch": self.kill_switch,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "VPNProfile":
        endpoint = payload.get("endpoint")
        endpoint_obj = None
        if endpoint:
            endpoint_obj = Endpoint(
                host=endpoint.get("host", ""),
                port=int(endpoint.get("port", 0)),
                protocol=endpoint.get("protocol", "udp"),
            )

        return cls(
            id=payload.get("id", ""),
            name=payload.get("name", "unnamed"),
            protocol=ProtocolType(payload.get("protocol", ProtocolType.WIREGUARD.value)),
            endpoint=endpoint_obj,
            username=payload.get("username"),
            password=payload.get("password"),
            config_path=payload.get("config_path"),
            dns=payload.get("dns"),
            mtu=payload.get("mtu"),
            allowed_ips=payload.get("allowed_ips"),
            auto_connect=bool(payload.get("auto_connect", False)),
            reconnect_policy=payload.get("reconnect_policy", "manual"),
            kill_switch=bool(payload.get("kill_switch", False)),
            metadata=payload.get("metadata"),
        )
