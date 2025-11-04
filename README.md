# DailyTicker

Python utility that gathers daily statistics for configured stock tickers, prints a console report, and sends a summary to a Telegram channel.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `config.example.yml` to `config.yml` and adjust the list of tickers as needed.
4. Copy `.env.example` to `.env` and provide `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` values.

## Usage

Run the report:

```bash
python -m src.main
```

Schedule this command externally (cron, systemd, etc.) to run daily.
