"""Financial indicators and metric calculations."""
from __future__ import annotations

import logging
from typing import Any, Dict

import numpy as np
import pandas as pd


def calculate_rsi(close_prices: pd.Series, period: int = 14) -> float | None:
    """Calculate the Relative Strength Index for a series of closing prices."""

    if len(close_prices) < period + 1:
        logging.warning("Not enough data to compute RSI (needs %s points).", period + 1)
        return None

    delta = close_prices.diff()
    gains = delta.clip(lower=0.0)
    losses = -delta.clip(upper=0.0)

    avg_gain = gains.rolling(window=period, min_periods=period).mean().iloc[-1]
    avg_loss = losses.rolling(window=period, min_periods=period).mean().iloc[-1]

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    if np.isnan(rsi):
        return None
    return float(rsi)


def calculate_percent_change(current: float, previous: float | None) -> float | None:
    """Calculate the percentage change from previous to current."""

    if previous in (None, 0):
        return None
    return float((current - previous) / previous * 100)


def summarize_metrics(ticker: str, history: pd.DataFrame, info: Dict[str, Any]) -> Dict[str, Any]:
    """Compute all metrics required for the daily report."""

    close_prices = history["Close"].dropna()
    current_price = float(close_prices.iloc[-1])

    rsi = calculate_rsi(close_prices)

    metrics: Dict[str, Any] = {
        "Ticker": ticker,
        "Price": current_price,
        "RSI14": rsi,
    }

    for window in (10, 30):
        shifted = close_prices.shift(window)
        past_price = shifted.iloc[-1]
        if pd.isna(past_price):
            logging.warning("Not enough data to compute %sd change for %s", window, ticker)
            change = None
        else:
            change = calculate_percent_change(current_price, float(past_price))
        metrics[f"Δ{window}d%"] = change

    metrics["Min30d"] = float(close_prices.min()) if not close_prices.empty else None
    metrics["Max30d"] = float(close_prices.max()) if not close_prices.empty else None

    rating = info.get("recommendationKey") if isinstance(info, dict) else None
    if rating:
        rating = str(rating).title()
    else:
        logging.warning("Analyst recommendation not available for %s", ticker)
        rating = None
    metrics["Rating"] = rating

    target_price = None
    if isinstance(info, dict):
        for key in ("targetMeanPrice", "targetMedianPrice", "targetHighPrice"):
            value = info.get(key)
            if isinstance(value, (int, float)):
                target_price = float(value)
                break
    if target_price is None:
        logging.warning("Target price not available for %s", ticker)
    metrics["Target"] = target_price

    target_diff = calculate_percent_change(target_price, current_price) if target_price is not None else None
    metrics["Target Δ%"] = target_diff

    return metrics
