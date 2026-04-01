import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a helpful language learning assistant that specializes in grammar correction.

When a user sends you a message:
1. Identify any grammar mistakes in their text
2. Provide the corrected version
3. Briefly explain what was wrong and why the correction is better
4. Offer encouragement to keep learning

If the text has no errors, compliment them and point out what they did well.
Be friendly, supportive, and educational in your responses.
Keep your explanations clear and concise."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Hello! I'm your language learning assistant.\n\n"
        "Send me any sentence or text, and I'll help you:\n"
        "- Correct grammar mistakes\n"
        "- Explain what was wrong\n"
        "- Help you improve your writing\n\n"
        "Just type something and I'll get started!"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "How to use this bot:\n\n"
        "Simply send me any text in English and I will:\n"
        "1. Check it for grammar errors\n"
        "2. Show you the corrected version\n"
        "3. Explain any mistakes\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)


async def correct_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    user_name = update.effective_user.first_name or "there"

    logger.info(f"Received message from {user_name}: {user_text[:50]}...")

    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Please check and correct this text:\n\n{user_text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )

        correction = response.choices[0].message.content
        await update.message.reply_text(correction)

    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        await update.message.reply_text(
            "Sorry, I encountered an error processing your message. Please try again."
        )


def main() -> None:
    logger.info("Starting language learning bot...")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, correct_grammar))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
