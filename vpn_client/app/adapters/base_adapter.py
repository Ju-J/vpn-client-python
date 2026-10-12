from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAdapter(ABC):
    def __init__(self, profile: Any, logger: Any) -> None:
        self.profile = profile
        self.logger = logger
        self.connected = False

    @abstractmethod
    def connect(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        raise NotImplementedError

    def update_state(self, state: str, message: str = "", **details: Any) -> None:
        self.logger.info(message or state, state=state, **details)
