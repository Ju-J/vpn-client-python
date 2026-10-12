from __future__ import annotations

from vpn_client.app.controllers.connection_state import ConnectionState
from vpn_client.app.controllers.vpn_manager import VPNManager
from vpn_client.app.models.profile import Endpoint, ProtocolType, VPNProfile


def _make_profile(protocol: ProtocolType) -> VPNProfile:
    return VPNProfile(
        id=f"demo-{protocol.value}",
        name=f"Demo {protocol.value}",
        protocol=protocol,
        endpoint=Endpoint(host="localhost", port=1194, protocol="udp"),
        config_path=f"{protocol.value}.conf",
    )


def test_vpn_manager_lifecycle_smoke() -> None:
    profile = _make_profile(ProtocolType.OPENVPN)
    manager = VPNManager([profile])

    result = manager.connect(profile.id)
    assert isinstance(result, bool)

    state = manager.status
    assert state in {
        ConnectionState.CONNECTING,
        ConnectionState.CONNECTED,
        ConnectionState.ERROR,
        ConnectionState.DISCONNECTED,
    }

    if manager.active_adapter is not None and state == ConnectionState.CONNECTED:
        health = manager.health_check()
        assert isinstance(health, bool)

    disconnect_result = manager.disconnect()
    assert isinstance(disconnect_result, bool)

    final_state = manager.status
    assert final_state in {
        ConnectionState.DISCONNECTED,
        ConnectionState.ERROR,
        ConnectionState.CONNECTED,
    }
