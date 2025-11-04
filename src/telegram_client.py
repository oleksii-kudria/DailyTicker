"""Simple Telegram client using the Bot API."""
from __future__ import annotations

import logging
from typing import Optional

import requests


class TelegramClient:
    """Sends messages to Telegram chats."""

    def __init__(self, token: Optional[str], chat_id: Optional[str]) -> None:
        self.token = token
        self.chat_id = chat_id

    def send_message(self, text: str) -> None:
        if not self.token or not self.chat_id:
            logging.info("Telegram credentials not provided. Skipping message send.")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            response = requests.post(url, data={"chat_id": self.chat_id, "text": text})
            if response.status_code != 200:
                logging.warning(
                    "Failed to send Telegram message: %s - %s", response.status_code, response.text
                )
        except requests.RequestException as exc:  # pragma: no cover - network failure handling
            logging.warning("Error sending Telegram message: %s", exc)
