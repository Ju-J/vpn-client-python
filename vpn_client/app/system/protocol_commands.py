from __future__ import annotations

from pathlib import Path
from typing import Any, List

from vpn_client.app.models.profile import ProtocolType, VPNProfile


def build_connect_command(profile: VPNProfile) -> list[str]:
    """Build a protocol-specific OS command for the VPN connection attempt.

    These are intentionally safe placeholders: they describe the native client or OS
    command the app should call, rather than re-implementing the protocol in Python.
    """
    host = profile.endpoint.host if profile.endpoint else "127.0.0.1"
    port = profile.endpoint.port if profile.endpoint else 443

    if profile.protocol == ProtocolType.WIREGUARD:
        config_path = profile.config_path or "wg0.conf"
        return ["wg.exe", "setconf", "VPN", str(Path(config_path))]

    if profile.protocol == ProtocolType.OPENVPN:
        config_path = profile.config_path or "client.ovpn"
        return ["openvpn.exe", "--config", str(Path(config_path)), "--verb", "3"]

    if profile.protocol == ProtocolType.SSH:
        if profile.username:
            return ["ssh", "-N", "-D", str(port), f"{profile.username}@{host}"]
        return ["ssh", "-N", "-D", str(port), host]

    if profile.protocol == ProtocolType.SOCKS5:
        return ["python", "-m", "socks5_proxy", "--host", host, "--port", str(port)]

    if profile.protocol == ProtocolType.SSTP:
        return ["rasdial", "VPN", profile.username or "", profile.password or ""]

    raise ValueError(f"Unsupported protocol for command generation: {profile.protocol}")


def build_disconnect_command(profile: VPNProfile) -> list[str]:
    if profile.protocol == ProtocolType.WIREGUARD:
        return ["wg.exe", "show"]
    if profile.protocol == ProtocolType.OPENVPN:
        return ["taskkill", "/F", "/IM", "openvpn.exe"]
    if profile.protocol == ProtocolType.SSH:
        return ["taskkill", "/F", "/IM", "ssh.exe"]
    if profile.protocol == ProtocolType.SOCKS5:
        return ["taskkill", "/F", "/IM", "python.exe"]
    if profile.protocol == ProtocolType.SSTP:
        return ["rasdial", "VPN", "/disconnect"]
    raise ValueError(f"Unsupported protocol for disconnect command: {profile.protocol}")


def build_health_check_command(profile: VPNProfile) -> list[str]:
    if profile.protocol == ProtocolType.WIREGUARD:
        return ["wg.exe", "show"]
    if profile.protocol == ProtocolType.OPENVPN:
        return ["tasklist", "/FI", "IMAGENAME eq openvpn.exe"]
    if profile.protocol == ProtocolType.SSH:
        return ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-T", profile.endpoint.host if profile.endpoint else "localhost"]
    if profile.protocol == ProtocolType.SOCKS5:
        return ["powershell", "-Command", "Test-NetConnection", "-ComputerName", (profile.endpoint.host if profile.endpoint else "localhost"), "-Port", str(profile.endpoint.port if profile.endpoint else 1080)]
    if profile.protocol == ProtocolType.SSTP:
        return ["rasdial"]
    raise ValueError(f"Unsupported protocol for health check: {profile.protocol}")


def build_cleanup_commands(profile: VPNProfile) -> list[list[str]]:
    """Return OS-level cleanup actions for a failed or disconnected tunnel."""
    cleanup: list[list[str]] = []

    if profile.protocol in {ProtocolType.WIREGUARD, ProtocolType.OPENVPN, ProtocolType.SSTP}:
        cleanup.append(["route", "delete", "0.0.0.0"])

    if profile.protocol == ProtocolType.SSH:
        cleanup.append(["taskkill", "/F", "/IM", "ssh.exe"])

    if profile.protocol == ProtocolType.SOCKS5:
        cleanup.append(["taskkill", "/F", "/IM", "python.exe"])

    return cleanup
