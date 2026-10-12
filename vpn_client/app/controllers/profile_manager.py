from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from vpn_client.app.models.profile import VPNProfile


class ProfileManager:
    def __init__(self, storage_path: Optional[str | Path] = None) -> None:
        self.storage_path = Path(storage_path) if storage_path else Path("config") / "profiles.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, profiles: List[VPNProfile]) -> None:
        payload = {"profiles": [profile.to_dict() for profile in profiles]}
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> List[VPNProfile]:
        if not self.storage_path.exists():
            return []
        raw = json.loads(self.storage_path.read_text(encoding="utf-8"))
        return [VPNProfile.from_dict(item) for item in raw.get("profiles", [])]

    def add(self, profile: VPNProfile, profiles: Optional[List[VPNProfile]] = None) -> List[VPNProfile]:
        bucket = profiles if profiles is not None else self.load()
        if not any(item.id == profile.id for item in bucket):
            bucket.append(profile)
        self.save(bucket)
        return bucket

    def remove(self, profile_id: str, profiles: Optional[List[VPNProfile]] = None) -> List[VPNProfile]:
        bucket = profiles if profiles is not None else self.load()
        filtered = [profile for profile in bucket if profile.id != profile_id]
        self.save(filtered)
        return filtered
