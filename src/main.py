"""Entry point for generating the daily stock statistics report."""
from __future__ import annotations

import logging
from typing import List

from .config import load_config
from .data_provider import DataProvider
from .formatter import format_detailed_messages, format_table
from .indicators import summarize_metrics
from .telegram_client import TelegramClient


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def run() -> None:
    configure_logging()
    config = load_config()
    data_provider = DataProvider()
    telegram = TelegramClient(config.telegram_bot_token, config.telegram_chat_id)

    results: List[dict] = []

    for ticker in config.tickers:
        try:
            ticker_data = data_provider.fetch(ticker)
            metrics = summarize_metrics(ticker_data.ticker, ticker_data.history, ticker_data.info)
            results.append(metrics)
        except Exception as exc:  # pragma: no cover - runtime protection
            logging.warning("Failed to process %s: %s", ticker, exc)
            continue

    if not results:
        logging.error("No results to display or send.")
        return

    table = format_table(results)
    print(table)

    messages = format_detailed_messages(results)
    for message in messages:
        telegram.send_message(message)


if __name__ == "__main__":
    run()
