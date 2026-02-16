# Telegram Bot API Template

Production-ready Telegram bot with agent orchestration.

## Quick Start

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Add your bot token to .env

# Run bot
python -m bot.main

# Run API server
uvicorn api.main:app --reload
```

## Structure

- `bot/` - Core bot functionality
- `agents/` - Agent orchestration
- `api/` - REST API
- `config/` - Configuration
- `tests/` - Test suite

## Features

- Multi-agent coordination
- Message routing
- Rate limiting
- Docker deployment
- REST API

## Docker

```bash
docker-compose up -d
```

## Config

Required env vars:

- `BOT_TOKEN` - Telegram bot token
- `ADMIN_USER_ID` - Admin user ID

## Test

```bash
pytest tests/ -v
```

## API Docs

Visit `http://localhost:8000/docs`
