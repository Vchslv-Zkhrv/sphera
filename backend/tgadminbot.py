import telegram as _telegram
from telegram import ext as _ext
from passlib import hash as _hash
import asyncio as _asyncio
import datetime as _dt

from config import TELEGRAM_ADMIN_BOT_TOKEN as _TOKEN, PASSWORD_SALT as _SALT
import emoji as _emoji
import time as _time
import models as _models
import tg as _tg


"""
Данный модуль должен быть запущен в отдельном потоке.
Обрабатывает сообщения, приходящие на https://t.me/sphere_admin_bot,
И делает записи в БД
"""


async def on_start(update: _telegram.Update, context: _ext.ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{_emoji.FLAME} Бот администраторов Проекта Сфера"
    )
    await on_help(update, context)


async def on_help(update: _telegram.Update, context: _ext.ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""Команды:

/help  =  посмотреть команды
/login  =  подписаться на уведомления для администраторов
/logout =  отписаться от рассылки
""")


async def on_add_admin(update: _telegram.Update, context: _ext.ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите логин и пароль от вашей учетной записи администратора на Проекте Сфера"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пример:"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="login: логин\npassword: пароль"
    )


async def on_admmin_auth(update: _telegram.Update, context: _ext.ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        rows = text.split("\n")
        login = rows[0].split("login: ")[1].strip()
        password = rows[1].split("password: ")[1].strip()
    except (IndexError, ValueError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Пароль и логин укаазаны неверно"
        )
        return
    if not login:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите логин корректно"
        )
        return
    if not password:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите пароль корректно"
        )
        return
    se = _dt.SessionLocal()
    try:
        admin = se.query(_models.Admin).filter_by(login=login).first()
        if not admin:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Логин неверный"
            )
            return
        if not _hash.bcrypt.verify(password + _SALT, admin.password):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Пароль неверный"
            )
            return
        admin.telegram = update.effective_chat.id
        se.commit()
        se.refresh(admin)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{_emoji.BLUE_HEART} Вы были успешно подписаны на рассылку уведомлений для админов"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{_emoji.WARNING} Удалите сообщение с логином и паролем!"
        )
    finally:
        se.close()


async def on_message(update: _telegram.Update, context: _ext.ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    text = update.message.text
    if text.startswith("/"):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Неверная команда"
        )
    elif "login: " in text and "password: " in text and len(text.split("\n")) == 2:
        await on_admmin_auth(update, context)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Неверная команда"
        )


async def on_logout(update: _telegram.Update, context: _ext.ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    se = _dt.SessionLocal()
    try:
        admin = se.query(_models.Admin).filter_by(telegram=update.effective_chat.id).first()
        if not admin:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{_emoji.ENRAGED_FACE} Вы не администратор!"
            )
            return
        admin.telegram = None
        se.commit()
        se.refresh(admin)
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{_emoji.WAVING_HAND} Вы были отписаны от рассылки уведомлений"
            )
    finally:
        se.close()


def run():
    application = _ext.ApplicationBuilder().token(_TOKEN).build()
    application.add_handler(_ext.CommandHandler("start", on_start))
    application.add_handler(_ext.CommandHandler("login", on_add_admin))
    application.add_handler(_ext.CommandHandler("help", on_help))
    application.add_handler(_ext.CommandHandler("logout", on_logout))
    application.add_handler(_ext.MessageHandler(_ext.filters.TEXT, on_message))
    application.run_polling()


if __name__ == '__main__':

    while True:
        try:
            run()
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            text = \
                f"{_emoji.WARNING} Телеграм-бот админов остановился {_emoji.WARNING}\n\n{e=}\n\n" + \
                "Попытка повторного запуска через 60 секунд."
            _asyncio.run(lambda: _tg.admin_broadcast(text))
            _time.sleep(60)
        finally:
            run()
