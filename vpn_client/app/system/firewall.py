from __future__ import annotations

import subprocess


class FirewallManager:
    def allow_udp(self, port: int) -> bool:
        result = subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=VPN_UDP_{port}", "dir=in", "action=allow", f"localport={port}", "protocol=UDP"], capture_output=True, text=True)
        return result.returncode == 0

    def allow_tcp(self, port: int) -> bool:
        result = subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=VPN_TCP_{port}", "dir=in", "action=allow", f"localport={port}", "protocol=TCP"], capture_output=True, text=True)
        return result.returncode == 0

