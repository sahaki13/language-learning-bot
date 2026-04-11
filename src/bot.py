import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config.settings import (
    TELEGRAM_TOKEN,
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    MAX_TOKENS,
    SUPPORTED_LANGUAGES,
)
from src.database.user_settings import (
    init_db,
    get_language, set_language,
    get_mode, set_mode,
    save_message,
)
from src.services.llm_service import LLMService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODE_LABELS = {
    "chat":         "💬 Chat only",
    "chat_grammar": "💬✅ Chat + Grammar",
    "grammar":      "✅ Grammar only",
}


class LanguageLearningBot:
    def __init__(self):
        self.llm = LLMService(GROQ_API_KEY, LLM_MODEL)
        init_db()

    def _language_keyboard(self) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
            for code, name in SUPPORTED_LANGUAGES.items()
        ]
        return InlineKeyboardMarkup(keyboard)

    def _mode_keyboard(self) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(label, callback_data=f"mode_{key}")]
            for key, label in MODE_LABELS.items()
        ]
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id

        lang_code = get_language(user_id)
        if not lang_code:
            await update.message.reply_text(
                "Chào bạn! Mình là bot luyện ngôn ngữ.\n\n"
                "Mình có thể hỗ trợ bạn:\n"
                "• Sửa lỗi ngữ pháp\n"
                "• Giải thích lỗi sai chi tiết\n"
                "• Trò chuyện để bạn luyện tập\n\n"
                "Bước đầu tiên: Hãy chọn ngôn ngữ bạn muốn luyện (mình sẽ nhớ cho bạn):",
                reply_markup=self._language_keyboard(),
            )
            return

        language_name = SUPPORTED_LANGUAGES.get(lang_code, lang_code)
        mode = get_mode(user_id)
        await update.message.reply_text(
            "Thiết lập đã sẵn sàng!\n\n"
            f"Ngôn ngữ hiện tại: <b>{language_name}</b>\n"
            f"Chế độ: <b>{MODE_LABELS.get(mode, mode)}</b>\n\n"
            "Bạn có thể gõ tin nhắn bất kỳ để bắt đầu luyện tập.\n"
            "Đổi ngôn ngữ: /settings | Đổi chế độ: /mode",
            parse_mode="HTML"
        )
        logger.info("User started bot: %s (ID: %s)", user.first_name, user_id)

    async def settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Chọn ngôn ngữ bạn muốn đổi sang vì hiện tại ngôn ngữ bạn quá gà:",
            reply_markup=self._language_keyboard(),
        )

    async def mode_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        current_mode = get_mode(user_id)
        await update.message.reply_text(
            f"Chế độ hiện tại: <b>{MODE_LABELS.get(current_mode, current_mode)}</b>\n\n"
            "Chọn chế độ bạn muốn:",
            reply_markup=self._mode_keyboard(),
            parse_mode="HTML"
        )

    async def language_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        language_code = query.data.split("_", 1)[1]
        user_id = update.effective_user.id

        if language_code not in SUPPORTED_LANGUAGES:
            await query.edit_message_text("Ngôn ngữ không hợp lệ.")
            return

        set_language(user_id, language_code)
        language_name = SUPPORTED_LANGUAGES[language_code]

        await query.edit_message_text(
            "Đã lưu ngôn ngữ thành công!\n\n"
            f"Ngôn ngữ hiện tại: <b>{language_name}</b>\n\n"
            "Giờ bạn có thể nhắn tin bình thường để luyện tập nhé.\n"
            "Đổi chế độ: /mode",
            parse_mode="HTML"
        )
        logger.info("User %s đã chọn ngôn ngữ: %s", user_id, language_code)

    async def mode_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        mode = query.data.split("_", 1)[1]
        user_id = update.effective_user.id

        if mode not in MODE_LABELS:
            await query.edit_message_text("Chế độ không hợp lệ.")
            return

        set_mode(user_id, mode)

        descriptions = {
            "chat":         "Mình sẽ chỉ trò chuyện, không kiểm tra ngữ pháp.",
            "chat_grammar": "Mình sẽ vừa kiểm tra ngữ pháp vừa trò chuyện.",
            "grammar":      "Mình sẽ chỉ kiểm tra ngữ pháp, không trò chuyện.",
        }
        await query.edit_message_text(
            f"✅ Đã chuyển sang chế độ: <b>{MODE_LABELS[mode]}</b>\n\n"
            f"{descriptions[mode]}",
            parse_mode="HTML"
        )
        logger.info("User %s đã chọn mode: %s", user_id, mode)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_message = (update.message.text or "").strip()

        language_code = get_language(user_id)
        if not language_code:
            await update.message.reply_text(
                "Bạn chưa chọn ngôn ngữ để luyện tập.\n\n"
                "Hãy chọn ngôn ngữ trước nhé:",
                reply_markup=self._language_keyboard(),
            )
            return

        language_name = SUPPORTED_LANGUAGES.get(language_code, language_code)
        mode = get_mode(user_id)

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING,
        )

        save_message(user_id, "user", user_message, language_code, mode)

        try:
            if mode in ("chat_grammar", "grammar"):
                grammar_result = await self.llm.check_grammar(user_message, language_name)
                if grammar_result.get("success"):
                    grammar_msg = grammar_result.get("content", "")
                    if "perfect" not in grammar_msg.lower() and "✅" not in grammar_msg:
                        await update.message.reply_text(
                            f"<b>Kiểm tra ngữ pháp:</b>\n\n{grammar_msg}",
                            parse_mode="HTML"
                        )
                        save_message(user_id, "bot", grammar_msg, language_code, mode)

            if mode in ("chat", "chat_grammar"):
                system_prompt = (
                    f"Bạn là một giáo viên dạy {language_name} cho người học tiếng Việt, thân thiện và khích lệ.\n\n"
                    f"Quy tắc trả lời:\n"
                    f"- Nếu người dùng nhắn bằng tiếng Việt: trả lời bằng tiếng Việt, giải thích/hỗ trợ về {language_name}\n"
                    f"- Nếu người dùng nhắn bằng {language_name}: trả lời bằng {language_name}, khích lệ họ tiếp tục\n"
                    f"- Chỉ trả lời tối đa 2-3 câu ngắn gọn\n"
                    f"- Luôn hỏi đúng MỘT câu hỏi liên quan để tiếp tục cuộc trò chuyện"
                )

                response_result = await self.llm.generate_response(
                    messages=[{"role": "user", "content": user_message}],
                    system_prompt=system_prompt,
                    temperature=LLM_TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                )

                if response_result.get("success"):
                    bot_reply = response_result.get("content", "")
                    await update.message.reply_text(bot_reply)
                    save_message(user_id, "bot", bot_reply, language_code, mode)
                else:
                    await update.message.reply_text("Mình đang gặp lỗi khi phản hồi. Bạn thử lại sau nhé!")
                    logger.warning("LLM response failed: %s", response_result.get("error"))

        except Exception:
            logger.exception("Lỗi xử lý tin nhắn cho user %s", user_id)
            await update.message.reply_text("Có lỗi xảy ra. Bạn thử lại sau một chút nhé.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "<b>Các lệnh có sẵn:</b>\n\n"
            "/start — Khởi động bot\n"
            "/settings — Đổi ngôn ngữ học\n"
            "/language — Đổi ngôn ngữ (cùng chức năng)\n"
            "/mode — Chọn chế độ (Chat / Grammar / Cả hai)\n"
            "/help — Xem trợ giúp này\n\n"
            "<b>Các chế độ:</b>\n"
            "💬 Chat only — Chỉ trò chuyện\n"
            "💬✅ Chat + Grammar — Vừa chat vừa sửa lỗi\n"
            "✅ Grammar only — Chỉ kiểm tra ngữ pháp"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")

    def setup(self) -> Application:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("settings", self.settings))
        app.add_handler(CommandHandler("language", self.settings))
        app.add_handler(CommandHandler("mode", self.mode_command))
        app.add_handler(CommandHandler("help", self.help_command))

        app.add_handler(CallbackQueryHandler(self.language_selected, pattern="^lang_"))
        app.add_handler(CallbackQueryHandler(self.mode_selected, pattern="^mode_"))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        return app

    async def run(self):
        import asyncio
        from telegram import BotCommand
        app = self.setup()
        logger.info("Bot đang khởi chạy và bạn vẫn vậy, vẫn không có ai yêu...")

        async with app:
            await app.initialize()
            await app.bot.set_my_commands([
                BotCommand("start",    "Khởi động bot"),
                BotCommand("settings", "Đổi ngôn ngữ học"),
                BotCommand("language", "Đổi ngôn ngữ học"),
                BotCommand("mode",     "Chọn chế độ (Chat / Grammar / Cả hai)"),
                BotCommand("help",     "Xem hướng dẫn sử dụng"),
            ])
            await app.start()
            await app.updater.start_polling()
            try:
                await asyncio.Event().wait()
            except (KeyboardInterrupt, SystemExit):
                pass
            finally:
                await app.updater.stop()
                await app.stop()
