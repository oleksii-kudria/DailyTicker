"""Provides market data for tickers using yfinance."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd
import yfinance as yf


@dataclass
class TickerData:
    """Represents fetched data for a ticker."""

    ticker: str
    history: pd.DataFrame
    info: Dict[str, Any]

    @property
    def current_price(self) -> float:
        return float(self.history["Close"].iloc[-1])


class DataProvider:
    """Fetches ticker data using the yfinance API."""

    def __init__(self, days: int = 30) -> None:
        self.days = days

    def fetch(self, ticker: str) -> TickerData:
        """Fetch historical price data and info for a ticker."""

        logging.info("Fetching data for %s", ticker)
        ticker_obj = yf.Ticker(ticker)

        try:
            history = ticker_obj.history(period=f"{self.days + 20}d", interval="1d")
        except Exception as exc:  # pragma: no cover - network failure handling
            logging.error("Failed to download history for %s: %s", ticker, exc)
            raise

        if history.empty:
            msg = f"No historical data returned for {ticker}"
            logging.error(msg)
            raise ValueError(msg)

        history = history.tail(self.days)
        history = history.sort_index()
        history = history.loc[:, [col for col in history.columns if col in {"Open", "High", "Low", "Close", "Volume"}]]

        info: Dict[str, Any] = {}
        try:
            info = ticker_obj.info or {}
        except Exception as exc:  # pragma: no cover - network failure handling
            logging.warning("Failed to fetch info for %s: %s", ticker, exc)

        return TickerData(ticker=ticker, history=history, info=info)
