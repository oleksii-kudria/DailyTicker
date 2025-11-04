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


def format_summary(rows: Iterable[Dict[str, Any]]) -> str:
    """Create a short textual summary for Telegram."""

    lines = ["Daily Stock Summary"]
    for row in rows:
        price = _format_value(row.get("Price"))
        rating = row.get("Rating") or "N/A"
        target_delta = _format_value(row.get("Target Δ%"))
        lines.append(f"{row.get('Ticker')}: Price {price}, Rating {rating}, Target Δ% {target_delta}")
    return "\n".join(lines)
