# vpn-client-python

This repository contains a starter project for a Windows VPN client written in Python.

It follows a layered architecture:
- UI layer
- controller / VPN manager
- protocol adapters
- Windows integration layer
- logging and diagnostics
- secure config and secret storage

This is an MVP foundation for a multi-protocol VPN client supporting:
- WireGuard
- OpenVPN
- SSH tunneling
- SOCKS5 proxy
- SSTP

## Structure

```
vpn_client/
  app/
    __init__.py
    main.py
    ui/
      __init__.py
      main_window.py
      tray.py
    controllers/
      __init__.py
      vpn_manager.py
      connection_state.py
      profile_manager.py
    adapters/
      __init__.py
      base_adapter.py
      wireguard_adapter.py
      openvpn_adapter.py
      ssh_adapter.py
      socks5_adapter.py
      sstp_adapter.py
    system/
      __init__.py
      windows_service.py
      process_runner.py
      routing.py
      dns_manager.py
      firewall.py
    security/
      __init__.py
      secret_store.py
      config_encryptor.py
    logging/
      __init__.py
      app_logger.py
      diagnostics.py
    models/
      __init__.py
      profile.py
      endpoint.py
      connection_event.py
  tests/
    __init__.py
    test_connection_state.py
    test_profile_model.py
  config/
    default_profiles.json
  tools/
    build_windows.py
    install_dependencies.py
  README.md
```

## Getting started

Use Python 3.11+

Install dependencies:

```bash
pip install PySide6 cryptography psutil
```

Run the app:

```bash
python -m vpn_client.app.main
```

## Roadmap

1. Foundation and project skeleton
2. Connection state machine and user interface
3. Protocol adapters
4. Windows integration (routes, DNS, firewall, service management)
5. Security and diagnostics
6. Packaging and installer

## Notes

This is a starter scaffold, not a complete production-ready VPN client.
The real-world implementation should rely on official native VPN clients or protocol-specific binaries for stability and correctness.
