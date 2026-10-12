from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, List, Optional


class WindowsServiceManager:
    def __init__(self, service_name: str = "vpn-client") -> None:
        self.service_name = service_name

    def start_service(self) -> bool:
        return self._run_windows_cmd(["sc", "start", self.service_name])

    def stop_service(self) -> bool:
        return self._run_windows_cmd(["sc", "stop", self.service_name])

    def query_service(self) -> str:
        result = subprocess.run(["sc", "query", self.service_name], capture_output=True, text=True)
        return result.stdout + result.stderr

    @staticmethod
    def _run_windows_cmd(command: List[str]) -> bool:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode == 0
