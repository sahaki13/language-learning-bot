import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============ TELEGRAM ============
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# ============ GROQ (LLM) ============
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))

# ============ DATABASE ============
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")

# ============ LOGGING ============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/bot.log"

# ============ SUPPORTED LANGUAGES ============
SUPPORTED_LANGUAGES = {
    "vi": "🇻🇳 Tiếng Việt",
    "ru": "🇷🇺 Русский (Russian)",
    "en": "🇬🇧 English"
}

# ============ LANGUAGES COMING SOON ============
# Sẽ thêm sau:
# "fr": "🇫🇷 Français",
# "de": "🇩🇪 Deutsch",
# "es": "🇪🇸 Español",
# "ja": "🇯🇵 日本語",

# ============ VALIDATION ============
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env file!")

if LLM_PROVIDER == "groq" and not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file!")

print("Configuration loaded successfully!")
