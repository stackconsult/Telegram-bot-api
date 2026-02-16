# Telegram Bot API Template

A production-ready Telegram bot API template for agent orchestration and multi-agent chat systems.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your bot token

# Run the bot
python -m bot.main

# Or run API server
uvicorn api.main:app --reload
```

## 📁 Structure

```text
bot/           # Core bot functionality
agents/        # Agent orchestration system
api/           # REST API endpoints
config/        # Configuration management
tests/         # Test suite
docker/        # Docker configuration
```

## 🤖 Agent Features

- Multi-agent coordination
- Chat group management
- Message routing
- Rate limiting
- Production deployment

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

## 📚 API Documentation

Visit `http://localhost:8000/docs` for interactive API docs.

## 🔧 Configuration

Key environment variables:

- `BOT_TOKEN` - Telegram bot token
- `WEBHOOK_URL` - Webhook URL (production)
- `ADMIN_USER_ID` - Admin Telegram user ID

## 🧪 Testing

```bash
pytest tests/ -v --cov=bot
```
