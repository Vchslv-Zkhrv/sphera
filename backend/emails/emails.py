import os as _os
import typing as _typing

import smtplib as _smtplib
import ssl as _ssl
from email.mime.text import MIMEText as _MIMEText
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.base import MIMEBase as _MIMEBase
from email import encoders as _encoders
from loguru import logger as _logger
import aiofiles as _aiofiles
import fastapi as _fastapi

from config import SMTP_LOGIN, SMTP_APPLICATION_PASSWORD, DOMAIN
import models as _models

"""
Рассылка сообщений по электронной почте

"""


async def get_verify_email_success_page():
    async with _aiofiles.open(
            f"{_os.getcwd()}/emails/templates/verify_email_success.html", "r", encoding="utf-8"
    ) as html:
        content = await html.read()
        content = content.replace("!SRC!", f"{DOMAIN}/api/images/email/")
        return _fastapi.responses.HTMLResponse(content=content)


def send_message(
        to: _typing.Union[_typing.List[str], str],
        message: str
):
    _logger.debug(f"new message: {to}")
    context = _ssl.create_default_context()
    try:
        with _smtplib.SMTP_SSL("smtp.yandex.ru", 465, timeout=5, context=context) as server:
            server.ehlo()
            server.login(SMTP_LOGIN, SMTP_APPLICATION_PASSWORD)
            server.sendmail(SMTP_LOGIN, to, message)
    except Exception as e:
        _logger.error(f"an exception occurred while sending the message: {e}")
    else:
        _logger.debug(f"sended successfuly: {to}")


async def send_verification_email(
        link: _models.Link,
        user: _models.User
):

    message = _MIMEMultipart()
    message["From"] = SMTP_LOGIN
    message["To"] = user.email
    message["Subject"] = "Регистрация аккаунта на Проекте Сфера"
    message["Bcc"] = SMTP_LOGIN

    async with _aiofiles.open(f"{_os.getcwd()}/emails/media/logo.png", 'rb') as f:
        mime = _MIMEBase('image', 'png', filename='logo.png')
        mime.add_header('Content-Disposition', 'attachment', filename='logo.png')
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', 'logo')
        mime.set_payload(await f.read())
        _encoders.encode_base64(mime)
        message.attach(mime)

    async with _aiofiles.open(f"{_os.getcwd()}/emails/templates/verify_email.html", "r", encoding="utf-8") as file:
        html = await file.read()
        html = html.replace("!HREF!", f"{DOMAIN}/api/verification/{link.url}")
        payload = _MIMEText(html, "HTML", "UTF-8")
        message.attach(payload)

    send_message(user.email, message.as_string())
