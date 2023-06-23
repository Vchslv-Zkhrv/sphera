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


static_logos = _typing.Literal["logo.png", "alter-logo.png"]
email_templates = _typing.Literal[
    "verify_email",
    "create_company_promice",
    "create_company_reject",
    "create_company_success",
    "update_company_promice",
    "update_company_reject",
    "update_company_success",
    "delete_company_promice",
    "delete_company_reject",
    "delete_company_success",
    "create_tags_promice",
    "create_tags_success",
    "create_tags_reject",
]
static_templates = _typing.Literal[
    "link_expired",
    "link_invalid",
    "link_overused",
    "link_join_useless",
    "verify_email_success",
    "account_not_activated",
    "internal_server_error"
]


async def get_static_page(
        template_name: static_templates,
        src: static_logos
):
    async with _aiofiles.open(
            f"{_os.getcwd()}/emails/templates/{template_name}.html", "r", encoding="utf-8"
    ) as html:
        content = await html.read()
        content = content.replace("!SRC!", f"{DOMAIN}/api/images/static/{src}")
        return _fastapi.responses.HTMLResponse(content=content)


async def get_verify_email_success_page():
    return await get_static_page("verify_email_success", "logo.png")


async def get_link_expired_page():
    return await get_static_page("link_expired", "alter-logo.png")


async def get_link_overused_page():
    return await get_static_page("link_overused", "alter-logo.png")


async def get_link_join_useless_page():
    return await get_static_page("link_join_useless", "alter-logo.png")


async def get_link_invalid_page():
    return await get_static_page("link_invalid", "alter-logo.png")


async def get_account_not_activated_page():
    return await get_static_page("account_not_activated", "alter-logo.png")


async def get_link_500_error_page():
    return await get_static_page("internal_server_error", "alter-logo.png")


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
