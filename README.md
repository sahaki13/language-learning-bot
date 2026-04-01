# Language Learning Telegram Bot

AI-powered language tutor bot for Vietnamese, Russian, and English.

## Setup

1. Clone repo:
git clone https://github.com/sahaki13/language-learning-bot cd language-learning-bot


2. Create `.env` file:
TELEGRAM_TOKEN=your_token_here GROQ_API_KEY=your_groq_key_here LLM_MODEL=mixtral-8x7b-32768 DATABASE_URL=sqlite:///bot.db


3. Install & run:
python -m venv venv source venv/bin/activate pip install -r requirements.txt python main.py


## Get Keys

- **Telegram Token**: Chat @BotFather → /newbot
- **Groq API**: https://console.groq.com/

## Deploy

[Replit] [Railway] [Docker]

