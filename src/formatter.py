"""Formatting utilities for displaying and messaging reports."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

_COLUMNS = [
    "Ticker",
    "Price",
    "RSI14",
    "Δ10d%",
    "Δ30d%",
    "Min30d",
    "Max30d",
    "Rating",
    "Target",
    "Target Δ%",
]


def _format_value(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def format_table(rows: Iterable[Dict[str, Any]]) -> str:
    """Format the metrics into a table for console output."""

    table_rows: List[List[str]] = []
    for row in rows:
        table_rows.append([_format_value(row.get(column)) for column in _COLUMNS])

    widths = [len(column) for column in _COLUMNS]
    for row in table_rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    header = " | ".join(column.ljust(widths[idx]) for idx, column in enumerate(_COLUMNS))
    separator = "-+-".join("-" * widths[idx] for idx in range(len(_COLUMNS)))
    body_lines = [" | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(row)) for row in table_rows]

    return "\n".join([header, separator, *body_lines]) if body_lines else header


def _format_percent_change(value: Any) -> str:
    if value is None:
        return "N/A"

    try:
        change = float(value)
    except (TypeError, ValueError):
        return str(value)

    emoji = ""
    if change >= 10:
        emoji = "🚀"
    elif change >= 5:
        emoji = "🔼"
    elif change <= -10:
        emoji = "💥"
    elif change <= -5:
        emoji = "🔽"

    return f"{change:+.2f}% {emoji}".rstrip()


def _format_rsi(value: Any) -> str:
    if value is None:
        return "N/A"

    try:
        rsi = float(value)
    except (TypeError, ValueError):
        return str(value)

    if rsi >= 70:
        return f"{rsi:.2f} 🔴 (High)"
    if rsi <= 30:
        return f"{rsi:.2f} 🔵 (Low)"
    return f"{rsi:.2f} 🟢"


def format_detailed_messages(rows: Iterable[Dict[str, Any]]) -> List[str]:
    """Create detailed per-ticker messages for Telegram delivery."""

    messages: List[str] = []
    for row in rows:
        ticker = row.get("Ticker", "Unknown")

        lines = [f"📈 {ticker}"]
        lines.append(f"• Price: {_format_value(row.get('Price'))}")
        lines.append(f"• RSI14: {_format_rsi(row.get('RSI14'))}")
        lines.append(f"• Δ10d%: {_format_percent_change(row.get('Δ10d%'))}")
        lines.append(f"• Δ30d%: {_format_percent_change(row.get('Δ30d%'))}")
        lines.append(f"• Min30d: {_format_value(row.get('Min30d'))}")
        lines.append(f"• Max30d: {_format_value(row.get('Max30d'))}")
        lines.append(f"• Rating: {_format_value(row.get('Rating'))}")
        lines.append(f"• Target: {_format_value(row.get('Target'))}")
        lines.append(f"• Target Δ%: {_format_percent_change(row.get('Target Δ%'))}")

        messages.append("\n".join(lines))

    return messages
