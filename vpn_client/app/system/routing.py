from __future__ import annotations

import subprocess
from typing import List


class RoutingManager:
    def get_routes(self) -> str:
        result = subprocess.run(["route", "print"], capture_output=True, text=True)
        return result.stdout + result.stderr

    def add_route(self, destination: str, gateway: str) -> bool:
        result = subprocess.run(["route", "add", destination, "mask", "255.255.255.0", gateway], capture_output=True, text=True)
        return result.returncode == 0

    def delete_route(self, destination: str) -> bool:
        result = subprocess.run(["route", "delete", destination], capture_output=True, text=True)
        return result.returncode == 0

