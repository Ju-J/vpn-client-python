from __future__ import annotations

import subprocess
from typing import Any, Optional

from vpn_client.app.logging.app_logger import AppLogger


class ProcessController:
    def __init__(self, logger: Optional[AppLogger] = None) -> None:
        self.logger = logger or AppLogger("vpn_client.process_controller")

    def start(self, command: list[str]) -> subprocess.Popen[str] | None:
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.logger.info("process_started", command=command, pid=proc.pid)
            return proc
        except FileNotFoundError as exc:
            self.logger.error("process_start_failed", command=command, error=str(exc))
            return None

    def stop(self, proc: subprocess.Popen[str] | None) -> bool:
        if proc is None:
            return True
        if proc.poll() is not None:
            return True
        proc.terminate()
        try:
            proc.wait(timeout=5)
            self.logger.info("process_stopped", pid=proc.pid)
            return True
        except subprocess.TimeoutExpired:
            proc.kill()
            self.logger.warning("process_killed", pid=proc.pid)
            return True
