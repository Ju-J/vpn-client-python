from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from typing import Any, Optional

from vpn_client.app.controllers.connection_state import ConnectionState, ConnectionStateMachine
from vpn_client.app.logging.app_logger import AppLogger


@dataclass
class HealthCheckResult:
    ok: bool
    message: str
    details: dict[str, Any] | None = None


class ProcessRunner:
    """Helper for launching protocol clients using subprocess."""

    def __init__(self, logger: Optional[AppLogger] = None) -> None:
        self.logger = logger or AppLogger("vpn_client.process")

    def run(self, command: list[str], timeout: int = 20) -> tuple[bool, str, str]:
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
            return result.returncode == 0, result.stdout, result.stderr
        except FileNotFoundError as exc:
            self.logger.error("process_not_found", command=command, error=str(exc))
            return False, "", str(exc)
        except subprocess.TimeoutExpired as exc:
            self.logger.error("process_timeout", command=command, error=str(exc))
            return False, exc.stdout or "", exc.stderr or str(exc)


class ConnectionHealthMonitor:
    def __init__(self, state_machine: ConnectionStateMachine, logger: Optional[AppLogger] = None) -> None:
        self.state_machine = state_machine
        self.logger = logger or AppLogger("vpn_client.health")
        self.runner = ProcessRunner(logger=self.logger)
        self.last_health: Optional[HealthCheckResult] = None

    def check(self, command: list[str], label: str) -> HealthCheckResult:
        ok, stdout, stderr = self.runner.run(command)
        if ok:
            message = f"{label} health check passed"
            result = HealthCheckResult(ok=True, message=message, details={"stdout": stdout, "stderr": stderr})
            self.last_health = result
            self.logger.info("health_check_passed", label=label)
            return result

        message = f"{label} health check failed"
        result = HealthCheckResult(ok=False, message=message, details={"stdout": stdout, "stderr": stderr})
        self.last_health = result
        self.state_machine.transition(ConnectionState.ERROR, message=message, details=result.details)
        self.logger.error("health_check_failed", label=label, error=message)
        return result


class ReconnectManager:
    def __init__(self, attempts: int = 3, delay_seconds: int = 5, logger: Optional[AppLogger] = None) -> None:
        self.attempts = attempts
        self.delay_seconds = delay_seconds
        self.logger = logger or AppLogger("vpn_client.reconnect")

    def retry(self, action, label: str = "connection") -> bool:
        for attempt in range(1, self.attempts + 1):
            self.logger.info("reconnect_attempt", label=label, attempt=attempt)
            if action():
                return True
            time.sleep(self.delay_seconds)
        self.logger.error("reconnect_exhausted", label=label, attempts=self.attempts)
        return False
