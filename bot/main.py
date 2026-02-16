"""
Main Telegram Bot Application
"""

import asyncio
import logging
from telegram.ext import Application
from config.settings import settings

logger = logging.getLogger(__name__)

class TelegramBot:
    """Production-ready Telegram bot"""
    
    def __init__(self):
        self.application = None
    
    async def initialize(self):
        """Initialize bot with webhook or polling"""
        self.application = Application.builder().token(settings.BOT_TOKEN).build()
        
        if settings.WEBHOOK_URL:
            await self.application.bot.set_webhook(settings.WEBHOOK_URL)
            logger.info(f"Webhook set to: {settings.WEBHOOK_URL}")
        else:
            logger.info("Running in polling mode")
    
    async def start(self):
        """Start the bot"""
        await self.application.initialize()
        await self.application.start()
        
        if settings.WEBHOOK_URL:
            await self.application.updater.start_webhook()
        else:
            await self.application.updater.start_polling()
    
    async def stop(self):
        """Stop the bot"""
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

async def main():
    """Main entry point"""
    bot = TelegramBot()
    try:
        await bot.initialize()
        await bot.start()
        
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await bot.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
