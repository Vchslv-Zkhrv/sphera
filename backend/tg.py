
import telegram as _telegram
from loguru import logger as _logger

from config import TELEGRAM_ADMIN_BOT_TOKEN
import models as _models
import database as _db

"""
Функции telegram-бота, доступные во время выполнения запросов fastapi.

"""


async def admin_broadcast(message):
    _logger.debug(f"new admin broadcast: {message}")
    try:
        se = _db.SessionLocal()
        bot = _telegram.Bot(TELEGRAM_ADMIN_BOT_TOKEN)
        async for admin in se.query(_models.Admin):
            if not admin.telegram:
                continue
            await bot.send_message(text=message, chat_id=admin.telegram)
    except Exception as e:
        _logger.debug(f"failed to broadcast: {e}")
    finally:
        se.close()
