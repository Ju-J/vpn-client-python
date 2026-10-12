from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class AppLogger:
    def __init__(self, name: str = "vpn_client", log_dir: Optional[str] = None) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

            if log_dir:
                log_path = Path(log_dir)
                log_path.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_path / "vpn_client.log", encoding="utf-8")
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def debug(self, message: str, **context: Any) -> None:
        self.logger.debug(self._format_message(message, context))

    def info(self, message: str, **context: Any) -> None:
        self.logger.info(self._format_message(message, context))

    def warning(self, message: str, **context: Any) -> None:
        self.logger.warning(self._format_message(message, context))

    def error(self, message: str, **context: Any) -> None:
        self.logger.error(self._format_message(message, context))

    def critical(self, message: str, **context: Any) -> None:
        self.logger.critical(self._format_message(message, context))

    @staticmethod
    def _format_message(message: str, context: Dict[str, Any]) -> str:
        if not context:
            return message
        return f"{message} | context={context}"


class DiagnosticsCollector:
    def __init__(self, log_dir: str) -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def collect_basic_snapshot(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "os": os.name,
            "cwd": os.getcwd(),
            "python_version": sys.version,
        }

    def save_snapshot(self, name: str, payload: Dict[str, Any]) -> Path:
        file_path = self.log_dir / f"{name}.json"
        file_path.write_text(str(payload), encoding="utf-8")
        return file_path
