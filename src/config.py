"""Application configuration loading."""
from __future__ import annotations

from dataclasses import dataclass
import logging
import os
from pathlib import Path
from typing import List

import yaml
from dotenv import load_dotenv


@dataclass
class AppConfig:
    """Represents configuration values used by the application."""

    tickers: List[str]
    telegram_bot_token: str | None
    telegram_chat_id: str | None


def load_config(config_path: str | os.PathLike[str] | None = None) -> AppConfig:
    """Load application configuration from YAML and environment variables."""

    load_dotenv()

    path = Path(config_path or os.environ.get("DAILY_TICKER_CONFIG", "config.yml"))
    if not path.exists():
        msg = f"Configuration file '{path}' was not found."
        logging.error(msg)
        raise FileNotFoundError(msg)

    with path.open("r", encoding="utf-8") as fp:
        data = yaml.safe_load(fp) or {}

    tickers = data.get("tickers") or []
    if not isinstance(tickers, list) or not all(isinstance(t, str) for t in tickers):
        msg = "Tickers must be provided as a list of strings in the configuration file."
        logging.error(msg)
        raise ValueError(msg)

    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    return AppConfig(
        tickers=[ticker.strip().upper() for ticker in tickers if ticker],
        telegram_bot_token=telegram_bot_token,
        telegram_chat_id=telegram_chat_id,
    )
