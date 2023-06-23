import telegram as _telegram
from loguru import logger as _logger

from config import TELEGRAM_ADMIN_BOT_TOKEN as _TOKEN
import models as _models
import database as _db
import emoji as _emoji


"""
Функции telegram-бота, доступные во время выполнения запросов fastapi.

"""


async def admin_broadcast(message: str):
    _logger.debug("new admin broadcast")
    try:
        se = _db.SessionLocal()
        bot = _telegram.Bot(_TOKEN)
        for admin in se.query(_models.Admin):
            if not admin.telegram:
                continue
            await bot.send_message(text=message, chat_id=admin.telegram)
    except Exception as e:
        _logger.debug(f"failed to broadcast: {e}")
    finally:
        se.close()


async def error(message: str):
    await admin_broadcast(f"{_emoji.WARNING} ОШИБКА НА СЕРВЕРЕ {_emoji.WARNING}\n\n" + message)


async def critical(message: str):
    await admin_broadcast(f"{_emoji.SKULL} КРИТИЧЕСКАЯ ОШИБКА НА СЕРВЕРЕ {_emoji.SKULL}\n\n" + message)


async def application(purpose: str, message: str):
    await admin_broadcast(f"{_emoji.BELL} НОВАЯ ЗАЯВКА {_emoji.BELL}\n\nЦель: {purpose}\n\n" + message)
