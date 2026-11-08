"""Structured local logging for chatbot interactions."""

import json
import logging
from datetime import datetime, timezone
from functools import lru_cache
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from helper_functions.config import PROJECT_ROOT, load_config


class _JsonLinesFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            **getattr(record, "payload", {"message": record.getMessage()}),
        }
        return json.dumps(entry, ensure_ascii=False, default=str)


@lru_cache(maxsize=1)
def _get_interaction_logger() -> logging.Logger:
    config = load_config()
    log_path = Path(config["LOG_FILE"])
    if not log_path.is_absolute():
        log_path = PROJECT_ROOT / log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("chatbot.interactions")
    logger.setLevel(getattr(logging, config["LOG_LEVEL"].upper()))
    logger.propagate = False

    resolved_path = str(log_path.resolve())
    if not any(
        getattr(handler, "baseFilename", None) == resolved_path
        for handler in logger.handlers
    ):
        handler = RotatingFileHandler(
            resolved_path,
            maxBytes=int(config.get("LOG_MAX_BYTES", 10_485_760)),
            backupCount=int(config.get("LOG_BACKUP_COUNT", 3)),
            encoding="utf-8",
        )
        handler.setFormatter(_JsonLinesFormatter())
        logger.addHandler(handler)
    return logger


def log_chat_interaction(
    *,
    interaction_id: str,
    query: str,
    retrieved_chunks: list[dict[str, Any]],
    response: str,
    error: dict[str, str] | None = None,
) -> None:
    """Write one complete chat turn, including any failure details, as JSONL."""
    entry = {
        "event": "chat_interaction",
        "interaction_id": interaction_id,
        "query": query,
        "retrieved_chunks": retrieved_chunks,
        "assistant_response": response,
        "error": error,
    }
    _get_interaction_logger().log(
        logging.ERROR if error else logging.INFO,
        "chat_interaction",
        extra={"payload": entry},
    )


def get_app_logger() -> logging.Logger:
    """Return the configured application logger."""
    return _get_interaction_logger()


def log_event(
    logger: logging.Logger,
    level: int,
    event: str,
    request_id: str,
    **details: Any,
) -> None:
    logger.log(
        level,
        event,
        extra={"payload": {"event": event, "request_id": request_id, **details}},
    )