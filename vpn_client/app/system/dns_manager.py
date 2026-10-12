from __future__ import annotations

import subprocess


class DNSManager:
    def get_dns(self) -> str:
        result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True)
        return result.stdout + result.stderr

    def set_dns(self, interface_name: str, dns_server: str) -> bool:
        result = subprocess.run(["netsh", "interface", "ip", "set", "dns", f"name={interface_name}", "source=static", f"address={dns_server}"], capture_output=True, text=True)
        return result.returncode == 0

