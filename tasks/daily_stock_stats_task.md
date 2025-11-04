# Codex Task: Daily Stock Statistics with Telegram Notification

## Objective

Create a **Python script** that collects and calculates daily statistics for selected stock tickers and sends the results to a Telegram channel.

---

## Stock List

The script must analyze the following tickers:

- `KYIV`
- `NVDA`
- `MSFT`
- `AMZN`

Tickers must be stored in a configuration file (`config.yml` or `.env`) — **not hardcoded** in the script.

---

## Data Source

Use any free API or library such as **`yfinance`** or a public stock data API.

For each ticker, retrieve:

- Current price (last/close)
- Daily OHLC data for the last **30 days**

---

## Metrics to Calculate

For each stock, compute:

1. **Current Price** – latest available close price.
2. **RSI (14-day)** – Relative Strength Index based on the last 14 days.
3. **Percentage Change** over:
   - Last 10 days
   - Last 30 days  
   Formula:  
   `change = (current_price - price_N_days_ago) / price_N_days_ago * 100`
4. **Highest and Lowest Prices** over the past 30 days.
5. **Analyst Recommendation** – aggregated rating (`Strong Buy`, `Buy`, `Hold`, `Sell`, etc.).
6. **Analyst Target Price** – average target price from analysts.
7. **Difference between Current and Target Price** (in %).  
   Formula:  
   `target_diff_pct = (target_price - current_price) / current_price * 100`

If data is unavailable for a metric, display `N/A` and log a warning.

---

## Console Output

Display a formatted table, for example:

```
Ticker | Price | RSI14 | Δ10d% | Δ30d% | Min30d | Max30d | Rating     | Target | Target Δ%
------ | ----- | ----- | ----- | ----- | ------ | ------ | ---------- | ------ | ----------
NVDA   | 123.4 | 65.2  |  5.3  | 12.7  | 110.0  | 130.5  | Buy        | 135.0  |  9.4
MSFT   | 401.2 | 55.1  |  1.1  |  3.5  | 380.0  | 410.0  | Strong Buy | 430.0  |  7.2
```

Errors for a specific ticker should not stop the entire report — skip and continue.

---

## Telegram Integration

After generating the report, send a summary message to a Telegram channel.

Environment variables to configure:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Use Telegram Bot API (`https://api.telegram.org/bot<TOKEN>/sendMessage`) or a library like `python-telegram-bot` or `aiogram`.

---

## Execution Frequency

- The script runs **once per day** (handled externally by `cron`, `systemd`, or Task Scheduler).
- No built-in scheduler is needed inside the script.

---

## Suggested Project Structure

```
project_root/
  README.md
  requirements.txt
  config.example.yml
  .env.example
  src/
    __init__.py
    config.py
    data_provider.py
    indicators.py
    formatter.py
    telegram_client.py
    main.py
```

---

## Logging & Error Handling

- Log all warnings and errors to console using Python's `logging` module.
- The script must continue execution if a single ticker fails.

---

## Acceptance Criteria

1. Running `python -m src.main` collects and prints a daily report.
2. Console output includes columns:  
   `Ticker, Price, RSI14, Δ10d%, Δ30d%, Min30d, Max30d, Rating, Target, Target Δ%`.
3. A Telegram message is successfully sent with summary results.
4. Secrets (API keys, tokens) are read from configuration or `.env`, not hardcoded.
5. Script handles missing data gracefully.
