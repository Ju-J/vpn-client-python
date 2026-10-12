from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Optional


class SecretStore:
    """A minimal local secret store. For production, prefer Windows DPAPI or Credential Manager."""

    def __init__(self, storage_path: str | Path = "secrets.json") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def set_secret(self, key: str, value: str) -> None:
        payload = self._load_payload()
        payload[key] = base64.b64encode(value.encode("utf-8")).decode("ascii")
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def get_secret(self, key: str) -> Optional[str]:
        payload = self._load_payload()
        encoded = payload.get(key)
        if encoded is None:
            return None
        return base64.b64decode(encoded.encode("ascii")).decode("utf-8")

    def _load_payload(self) -> dict[str, str]:
        if not self.storage_path.exists():
            return {}
        try:
            raw = self.storage_path.read_text(encoding="utf-8")
            if not raw.strip():
                return {}
            data = json.loads(raw)
            if not isinstance(data, dict):
                return {}
            return {str(k): str(v) for k, v in data.items()}
        except Exception:
            return {}
