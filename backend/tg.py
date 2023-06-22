from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from config import TELEGRAM_MAIN_BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Добро пожаловать на Проект Сфера. Выберите действие"
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_MAIN_BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()
