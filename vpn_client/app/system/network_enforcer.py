from __future__ import annotations

import subprocess
from typing import Any, Optional

from vpn_client.app.logging.app_logger import AppLogger


class WindowsNetworkEnforcer:
    """Thin wrapper for Windows route/DNS/firewall operations used by the app."""

    def __init__(self, logger: Optional[AppLogger] = None) -> None:
        self.logger = logger or AppLogger("vpn_client.network")

    def run(self, command: list[str]) -> tuple[bool, str, str]:
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except FileNotFoundError as exc:
            self.logger.error("windows_command_missing", command=command, error=str(exc))
            return False, "", str(exc)

    def set_dns(self, interface_name: str, dns_server: str) -> bool:
        ok, stdout, stderr = self.run(["netsh", "interface", "ip", "set", "dns", f"name={interface_name}", "source=static", f"address={dns_server}"])
        self.logger.info("dns_set", interface_name=interface_name, dns_server=dns_server, ok=ok, stdout=stdout, stderr=stderr)
        return ok

    def add_route(self, destination: str, gateway: str) -> bool:
        ok, stdout, stderr = self.run(["route", "add", destination, "mask", "255.255.255.0", gateway])
        self.logger.info("route_added", destination=destination, gateway=gateway, ok=ok, stdout=stdout, stderr=stderr)
        return ok

    def delete_route(self, destination: str) -> bool:
        ok, stdout, stderr = self.run(["route", "delete", destination])
        self.logger.info("route_deleted", destination=destination, ok=ok, stdout=stdout, stderr=stderr)
        return ok

    def allow_udp(self, port: int) -> bool:
        ok, stdout, stderr = self.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=VPN_UDP_{port}", "dir=in", "action=allow", f"localport={port}", "protocol=UDP"])
        self.logger.info("udp_allowed", port=port, ok=ok, stdout=stdout, stderr=stderr)
        return ok

    def allow_tcp(self, port: int) -> bool:
        ok, stdout, stderr = self.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=VPN_TCP_{port}", "dir=in", "action=allow", f"localport={port}", "protocol=TCP"])
        self.logger.info("tcp_allowed", port=port, ok=ok, stdout=stdout, stderr=stderr)
        return ok
