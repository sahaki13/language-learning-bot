# language-learning-bot

AI-powered Telegram bot for language learning with grammar correction.

## Overview

This is a Python Telegram bot that uses OpenAI's GPT-4o-mini to help users learn languages by correcting their grammar. Users send a message to the bot, and it responds with corrections, explanations, and encouragement.

## Tech Stack

- **Language**: Python 3.11
- **Telegram Library**: python-telegram-bot 22.7
- **AI**: OpenAI API (GPT-4o-mini)
- **Environment**: Replit (NixOS, stable-25_05)

## Project Structure

```
bot.py            # Main bot entry point
requirements.txt  # Python dependencies
```

## Required Secrets

- `TELEGRAM_BOT_TOKEN` — From @BotFather on Telegram
- `OPENAI_API_KEY` — From https://platform.openai.com/api-keys

## Running

The bot runs as a console workflow (`python bot.py`) using long-polling to receive Telegram messages.

## Bot Features

- `/start` — Welcome message with usage instructions
- `/help` — Help message with command list
- Any text message — Grammar correction with explanation
