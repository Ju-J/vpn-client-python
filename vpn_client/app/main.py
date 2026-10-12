from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from vpn_client.app.controllers.connection_state import ConnectionState, ConnectionStateMachine
from vpn_client.app.logging.app_logger import AppLogger
from vpn_client.app.models.profile import ProtocolType, VPNProfile


def create_default_profiles() -> List[VPNProfile]:
    return [
        VPNProfile(
            id="wg-demo",
            name="WireGuard Demo",
            protocol=ProtocolType.WIREGUARD,
            endpoint=None,
            dns="1.1.1.1",
            auto_connect=False,
            kill_switch=True,
        ),
        VPNProfile(
            id="ssh-demo",
            name="SSH Tunnel Demo",
            protocol=ProtocolType.SSH,
            endpoint=None,
            dns="8.8.8.8",
            auto_connect=False,
            kill_switch=False,
        ),
    ]


def save_default_profiles(file_path: str | Path) -> None:
    profiles = create_default_profiles()
    payload = {"profiles": [profile.to_dict() for profile in profiles]}
    Path(file_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def sample_main() -> None:
    logger = AppLogger("vpn_client")
    state = ConnectionStateMachine()
    logger.info("app_started", state=state.state.value)
    print("VPN client runtime scaffold initialized.")

    default_profiles = create_default_profiles()
    print([profile.name for profile in default_profiles])

