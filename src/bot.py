from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import logging

# from src.handlers.start_handler import StartHandler
# from src.handlers.message_handler import MessageHandler as MsgHandler
# from src.handlers.language_handler import LanguageHandler
from src.services.llm_service import LLMService
from config.settings import (
    TELEGRAM_TOKEN,
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    MAX_TOKENS,
    SUPPORTED_LANGUAGES
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LanguageLearningBot:
    def __init__(self):
        self.llm = LLMService(GROQ_API_KEY, LLM_MODEL)
        self.user_languages = {}  # {user_id: language_code}
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_msg = f"""
Welcome, {user.first_name}!

I'm your AI Language Tutor Bot!

**What I can do:**
Chat with you in any language
Correct your grammar errors
Explain your mistakes
Help you practice naturally

**Let's get started!**
Type /language to choose a language
        """
        
        await update.message.reply_text(welcome_msg)
        logger.info(f"User started bot: {user.first_name} (ID: {user.id})")
    
    async def language_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show language selection menu"""
        
        # Create buttons
        keyboard = []
        for code, lang_name in SUPPORTED_LANGUAGES.items():
            keyboard.append([
                InlineKeyboardButton(lang_name, callback_data=f"lang_{code}")
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "**Choose a language to learn:**",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    async def language_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection"""

        query = update.callback_query
        await query.answer()
        
        # Extract language code
        language_code = query.data.split("_")[1]
        user_id = update.effective_user.id
        
        # Save user's language choice
        self.user_languages[user_id] = language_code
        language_name = SUPPORTED_LANGUAGES[language_code]
        
        # Send confirmation
        await query.edit_message_text(
            f"**Great!** You're learning {language_name}!\n\n"
            f"Now just start chatting and I'll help you improve!\n\n"
            f"Just type your message in {language_name} and I will:\n"
            f"1️. Check your grammar\n"
            f"2️. Reply naturally\n"
            f"3️. Explain any mistakes",
            parse_mode="Markdown"
        )
        
        logger.info(f"User {user_id} selected language: {language_code}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages"""
        
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Check if user has selected language
        if user_id not in self.user_languages:
            await update.message.reply_text(
                "Please set your learning language first!\n\n"
                "Type /language to choose a language."
            )
            return
        
        language_code = self.user_languages[user_id]
        language_name = SUPPORTED_LANGUAGES[language_code]
        
        # Show typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )
        
        try:
            # Step 1: Check grammar
            logger.info(f"Checking grammar for user {user_id}...")
            
            grammar_result = await self.llm.check_grammar(user_message, language_name)
            
            if grammar_result["success"]:
                # Send grammar feedback
                grammar_msg = grammar_result["content"]
                
                if "Perfect" not in grammar_msg:
                    await update.message.reply_text(
                        f"**Grammar Check:**\n\n{grammar_msg}",
                        parse_mode="Markdown"
                    )
                else:
                    logger.info(f"Grammar is perfect for user {user_id}")
            
            # Step 2: Generate conversational response
            logger.info(f"Generating response for user {user_id}...")
            
            system_prompt = f"""You are a friendly language tutor helping someone learn {language_name}.
Keep your responses:
- Natural and conversational
- 2-3 sentences
- Encouraging and fun
- Ask follow-up questions

Respond in {language_name}."""
            
            response_result = await self.llm.generate_response(
                messages=[{"role": "user", "content": user_message}],
                system_prompt=system_prompt,
                temperature=LLM_TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            
            if response_result["success"]:
                await update.message.reply_text(response_result["content"])
                logger.info(f"Response sent to user {user_id}")
            else:
                await update.message.reply_text(
                    "Sorry, I had trouble responding. Please try again."
                )
                logger.error(f"Response generation failed: {response_result['error']}")
        
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await update.message.reply_text(
                "An error occurred. Please try again later."
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        
        help_msg = """
**Commands:**
/start - Start the bot
/language - Choose a language
/help - Show this help message

**How to use:**
1. Choose a language with /language
2. Type messages in that language
3. I'll check your grammar and reply
4. Learn by practicing!
        """
        
        await update.message.reply_text(help_msg, parse_mode="Markdown")
    
    def setup(self) -> Application:
        """Setup bot with handlers"""
        
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Command handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("language", self.language_menu))
        app.add_handler(CommandHandler("help", self.help_command))
        
        # Callback handlers for buttons
        app.add_handler(CallbackQueryHandler(
            self.language_selected,
            pattern="^lang_"
        ))
        
        # Message handler
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))
        
        return app
    
    async def run(self):
        """Run the bot"""
        import asyncio
        app = self.setup()
        logger.info("Bot is starting...")

        async with app:
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            try:
                await asyncio.Event().wait()
            except (KeyboardInterrupt, SystemExit):
                pass
            finally:
                await app.updater.stop()
                await app.stop()

if __name__ == "__main__":
    import asyncio
    bot = LanguageLearningBot()
    asyncio.run(bot.run())