"""Entry point for generating the daily stock statistics report."""
from __future__ import annotations

import argparse
import logging
from typing import List, Sequence

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


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for selecting output targets."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--console",
        action="store_true",
        help="Print the generated report to the console.",
    )
    parser.add_argument(
        "--telegram",
        action="store_true",
        help="Send the generated report via Telegram.",
    )
    return parser.parse_args(argv)


def run(argv: Sequence[str] | None = None) -> None:
    configure_logging()
    args = parse_args(argv)

    targets_specified = args.console or args.telegram
    send_to_console = args.console or not targets_specified
    send_to_telegram = args.telegram or not targets_specified

    config = load_config()
    data_provider = DataProvider()
    telegram: TelegramClient | None = None
    if send_to_telegram:
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
    if send_to_console:
        print(table)

    if send_to_telegram and telegram is not None:
        messages = format_detailed_messages(results)
        for message in messages:
            telegram.send_message(message)


if __name__ == "__main__":
    run()
