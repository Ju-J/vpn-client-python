from __future__ import annotations

from vpn_client.app.models.profile import VPNProfile, ProtocolType


def test_profile_round_trip() -> None:
    profile = VPNProfile(
        id="p1",
        name="Test VPN",
        protocol=ProtocolType.OPENVPN,
        username="demo",
        password="secret",
        dns="1.1.1.1",
        mtu=1420,
        allowed_ips=["0.0.0.0/0"],
        reconnect_policy="auto",
        kill_switch=True,
    )
    payload = profile.to_dict()
    restored = VPNProfile.from_dict(payload)
    assert restored.id == profile.id
    assert restored.protocol == profile.protocol
    assert restored.dns == profile.dns
    assert restored.kill_switch is True


def test_connection_state_machine() -> None:
    from vpn_client.app.controllers.connection_state import ConnectionState, ConnectionStateMachine

    machine = ConnectionStateMachine()
    machine.transition(ConnectionState.CONNECTING, protocol="wireguard", message="connect")
    assert machine.state == ConnectionState.CONNECTING
    machine.reset()
    assert machine.state == ConnectionState.DISCONNECTED

