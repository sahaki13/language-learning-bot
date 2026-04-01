import asyncio
import logging
import os
from src.bot import LanguageLearningBot

# Setup logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main entry point"""
    logger.info("=" * 50)
    logger.info("Starting Language Learning Bot...")
    logger.info("=" * 50)
    
    try:
        bot = LanguageLearningBot()
        await bot.run()
    
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main())