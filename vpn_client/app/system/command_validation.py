from __future__ import annotations

import shutil
from typing import Any, Iterable, Sequence

from vpn_client.app.models.profile import VPNProfile
from vpn_client.app.system.protocol_commands import build_connect_command, build_disconnect_command, build_health_check_command


class CommandValidator:
    """Check that required native commands are available before connecting."""

    @staticmethod
    def validate_profile(profile: VPNProfile) -> list[str]:
        errors: list[str] = []
        connect_cmd = build_connect_command(profile)
        if connect_cmd:
            binary = connect_cmd[0]
            if shutil.which(binary) is None:
                errors.append(f"Required native binary not found: {binary}")

        health_cmd = build_health_check_command(profile)
        if health_cmd:
            health_binary = health_cmd[0]
            if shutil.which(health_binary) is None:
                errors.append(f"Health-check binary not found: {health_binary}")

        return errors

    @staticmethod
    def validate_command(command: Sequence[str]) -> list[str]:
        if not command:
            return ["Empty command"]
        binary = command[0]
        if shutil.which(binary) is None:
            return [f"Command binary not found: {binary}"]
        return []


class SafeProtocolExecutor:
    """Wrap protocol command generation with validation before execution."""

    def __init__(self) -> None:
        self.validator = CommandValidator()

    def prepare(self, profile: VPNProfile) -> tuple[bool, list[str], list[str]]:
        connect_errors = self.validator.validate_profile(profile)
        disconnect_errors = self.validator.validate_command(build_disconnect_command(profile))
        return (not connect_errors and not disconnect_errors, connect_errors, disconnect_errors)
