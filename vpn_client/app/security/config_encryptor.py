from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigEncryptor:
    """Minimal configuration encryptor placeholder.

    Production should use Windows DPAPI / Credential Manager or a platform keyring.
    """

    @staticmethod
    def encrypt(payload: dict[str, Any]) -> str:
        return json.dumps(payload, indent=2)

    @staticmethod
    def decrypt(blob: str) -> dict[str, Any]:
        return json.loads(blob)

    @staticmethod
    def write_encrypted(path: str | Path, payload: dict[str, Any]) -> None:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(ConfigEncryptor.encrypt(payload), encoding="utf-8")

    @staticmethod
    def read_encrypted(path: str | Path) -> dict[str, Any]:
        file_path = Path(path)
        if not file_path.exists():
            return {}
        return ConfigEncryptor.decrypt(file_path.read_text(encoding="utf-8"))
