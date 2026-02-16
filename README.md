# Telegram Bot API Template

Production-ready Telegram bot with comprehensive API components and agent orchestration.

## 🚀 Quick Start

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

## 📁 Structure

```
bot/                    # Core bot functionality
├── main.py             # Main bot entrypoint
├── handlers/           # Message and command handlers
├── middleware/         # Custom middleware
└── utils/             # Utility functions

agents/                 # Agent orchestration system
├── base.py            # Base agent classes
├── manager.py         # Agent lifecycle management
└── chat_groups.py     # Multi-agent chat coordination

api/                    # REST API endpoints
├── main.py            # FastAPI application
├── components/        # API components and patterns
├── handlers/          # Request handlers
└── models/            # Pydantic models

telegram_api/          # Comprehensive Telegram API library
├── core.py            # Core bot system
├── handlers/          # All Telegram update handlers
├── models/            # Data models (Telegram & Database)
├── services/          # API and database services
├── utils/             # Utilities and helpers
└── exceptions.py      # Custom exceptions

config/                 # Configuration management
├── settings.py        # Application settings
└── logging.py         # Logging configuration

tests/                  # Test suite
├── test_basic.py      # Core functionality tests
├── test_agents.py     # Agent system tests
└── test_comprehensive.py # Full integration tests
```

## 🤖 Features

### Core Bot Features

- **Multi-mode operation**: Polling or webhook modes
- **Update processing**: Handle all Telegram update types
- **Command system**: Extensible command framework
- **Message handling**: Text, media, and special messages
- **Rate limiting**: Built-in protection against abuse
- **Error handling**: Comprehensive error management

### Agent System

- **Agent orchestration**: Multi-agent coordination
- **Chat groups**: Agent collaboration in groups
- **Message routing**: Intelligent message distribution
- **Lifecycle management**: Start, stop, and monitor agents

### API Components

- **Complete Telegram API**: All Bot API 6.0+ methods
- **Database integration**: SQLAlchemy models and services
- **Authentication**: JWT-based auth system
- **Rate limiting**: Redis-based rate limiting
- **Middleware**: Security, logging, CORS, validation

### Production Features

- **Docker deployment**: Multi-container setup
- **Monitoring**: Prometheus metrics and health checks
- **Logging**: Structured logging with multiple levels
- **Testing**: Comprehensive test suite
- **Documentation**: Complete API documentation

## 🛠️ Installation

### Requirements

- Python 3.8+
- PostgreSQL (optional, for persistent storage)
- Redis (optional, for caching and rate limiting)

### Setup

```bash
# Clone the repository
git clone https://github.com/stackconsult/Telegram-bot-api
cd Telegram-bot-api

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run tests
pytest tests/ -v
```

## 🔧 Configuration

### Environment Variables

```bash
# Bot Configuration
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-domain.com/webhook
WEBHOOK_PATH=/webhook
ADMIN_USER_ID=123456789

# Database
DATABASE_URL=postgresql://user:password@localhost/botdb
REDIS_URL=redis://localhost:6379

# Application
LOG_LEVEL=INFO
ENVIRONMENT=production
RATE_LIMIT_PER_MINUTE=30
```

## 📚 API Documentation

### REST API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/bot/status` - Bot status
- `POST /api/v1/bot/message` - Send message
- `GET /api/v1/agents/list` - List agents
- `GET /api/v1/groups/list` - List chat groups

### Interactive Docs

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🤖 Bot Commands

### Basic Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/status` - Check bot status
- `/agents` - List available agents

### Admin Commands

- `/admin` - Admin panel
- `/restart` - Restart the bot
- `/logs` - View recent logs

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=telegram_api --cov-report=html

# Run specific test file
pytest tests/test_basic.py -v
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Services

- **bot-api**: Main application
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **nginx**: Reverse proxy (optional)
- **prometheus**: Monitoring
- **grafana**: Dashboard

## 📊 Monitoring

### Metrics

- Bot status and health
- Message processing rates
- Agent performance
- Error rates and types
- Database performance

### Health Checks

- Application health: `GET /health`
- Database connectivity
- Redis connectivity
- External API status

## 🔒 Security

### Features

- **Authentication**: JWT-based API auth
- **Rate limiting**: Per-user and global limits
- **Input validation**: Comprehensive input sanitization
- **CORS protection**: Configurable CORS headers
- **Security headers**: XSS, CSRF, clickjacking protection

### Best Practices

- Use environment variables for secrets
- Enable rate limiting in production
- Monitor logs for suspicious activity
- Keep dependencies updated

## 🚀 Deployment

### Production Checklist

- [ ] Configure environment variables
- [ ] Set up PostgreSQL database
- [ ] Configure Redis cache
- [ ] Set up SSL certificates
- [ ] Configure monitoring
- [ ] Set up log rotation
- [ ] Test all functionality
- [ ] Run security scans

### Platforms

- **Railway**: Deploy with one click
- **Render**: Free tier available
- **AWS**: ECS or Lambda
- **Google Cloud**: Cloud Run
- **DigitalOcean**: App Platform

## 📖 Advanced Usage

### Custom Agents

```python
from telegram_api.base import BaseAgent

class MyAgent(BaseAgent):
    async def process_message(self, message):
        # Custom logic here
        return "Response from my agent"
```

### Database Integration

```python
from telegram_api.services.database_service import ServiceFactory

# Initialize services
factory = ServiceFactory()
await factory.initialize()

# Get user service
user_service = factory.get_service("user")
user = await user_service.get_or_create_user(telegram_user)
```

### Custom Handlers

```python
from telegram_api.handlers import MessageHandler

class CustomMessageHandler(MessageHandler):
    async def handle(self, update, context):
        # Custom message handling
        pass
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run test suite
6. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Repository](https://github.com/stackconsult/Telegram-bot-api)

## 🆘 Support

For issues and questions:

- Create an issue in this repository
- Check the documentation
- Review existing issues

---

**Version**: 1.0.0  
**Last Updated**: 2025-02-16  
**Compatible**: Python 3.8+, Telegram Bot API 6.0+
