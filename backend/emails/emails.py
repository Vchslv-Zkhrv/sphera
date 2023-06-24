import os as _os
import typing as _typing

import smtplib as _smtplib
import ssl as _ssl
from email.mime.text import MIMEText as _MIMEText
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.base import MIMEBase as _MIMEBase
from email import encoders as _encoders
from email.message import Message as _Message
from loguru import logger as _logger
import aiofiles as _aiofiles

from config import SMTP_LOGIN as _LOGIN, SMTP_APPLICATION_PASSWORD as _PASSWORD, DOMAIN as _DOMAIN
import models as _models
import tg as _tg
import schemas as _schemas


"""
Рассылка сообщений по электронной почте

"""


async def send_message(
        to: _typing.Union[_typing.List[str], str],
        message: str
):
    _logger.debug(f"new message: {to}")
    context = _ssl.create_default_context()
    try:
        with _smtplib.SMTP_SSL("smtp.yandex.ru", 465, timeout=5, context=context) as server:
            server.ehlo()
            server.login(_LOGIN, _PASSWORD)
            server.sendmail(_LOGIN, to, message)
    except Exception as e:
        _logger.error(f"an exception occurred while sending the message: {e}")
        await _tg.error(f"Не удалось отправить сообщение.\n{to=}\n{e=}")
    else:
        _logger.debug(f"sended successfuly: {to}")


async def _attach_logo(message: _Message, logo: _schemas.static_logos):
    async with _aiofiles.open(f"{_os.getcwd()}/data/logos/{logo}", 'rb') as f:
        mime = _MIMEBase('image', 'png', filename='logo.png')
        mime.add_header('Content-Disposition', 'attachment', filename='logo.png')
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', 'logo')
        mime.set_payload(await f.read())
        _encoders.encode_base64(mime)
        message.attach(mime)
    return message


def _get_message(to: str, subject: str):
    message = _MIMEMultipart()
    message["From"] = _LOGIN
    message["To"] = to
    message["Subject"] = subject
    message["Bcc"] = _LOGIN
    return message


async def _create_message(
        to: str,
        subject: str,
        logo: _schemas.static_logos,
        template: _schemas.email_templates,
        **replaces
):
    message = _get_message(to, subject)
    message = await _attach_logo(message, logo)
    message = await _attach_template(message, template, **replaces)
    await send_message(to, message.as_string())


async def _attach_template(message: _Message, template: _schemas.email_templates, **replace):

    async with _aiofiles.open(f"{_os.getcwd()}/emails/templates/{template}.html", "r", encoding="utf-8") as file:
        html = await file.read()
        for key, value in replace.items():
            html = html.replace(f"!{key.upper()}!", value)
        payload = _MIMEText(html, "HTML", "UTF-8")
        message.attach(payload)
    return message


async def send_verification_email(
        link: _models.Link,
        user: _models.User
):
    await _create_message(
        to=user.email,
        subject="Регистрация аккаунта на Проекте Сфера",
        logo="logo.png",
        template="verify_email",
        href=f"{_DOMAIN}/api/verification/{link.url}"
    )


async def send_create_company_promise_email(to: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на регистрацию учебного заведения",
        logo="logo.png",
        template="create_company_promise"
    )


async def send_create_company_success_email(to: str, company: _models.Company):
    await _create_message(
        to=to,
        subject="Ответ по заявке на регистрацию учебного заведения",
        logo="logo.png",
        template="create_company_success",
        href=f"{_DOMAIN}/api/companies/{company.id}"
    )


async def send_create_company_reject_email(to: str, reason: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на регистрацию учебного заведения",
        logo="logo.png",
        template="create_company_reject",
        reason=reason
    )


async def send_update_company_promise_email(to: str, company: _models.Company):
    await _create_message(
        to=to,
        subject="Ответ по заявке на изменение данных учебного заведения",
        logo="logo.png",
        template="update_company_promise",
        company=company
    )


async def send_update_company_reject_email(to: str, company: _models.Company, reason: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на изменение данных учебного заведения",
        logo="logo.png",
        template="update_company_reject",
        company=company.name,
        reason=reason
    )


async def send_update_company_success_email(to: str, company: _models.Company):
    await _create_message(
        to=to,
        subject="Ответ по заявке на изменение данных учебного заведения",
        logo="logo.png",
        template="update_company_success",
        company=company.name,
        href=f"{_DOMAIN}/api/companies/{company.id}"
    )


async def send_delete_company_promise_email(to: str, company: _models.Company):
    await _create_message(
        to=to,
        subject="Ответ по заявке на удаление учебного заведения с сайта Проекта Сфера",
        logo="logo.png",
        template="delete_company_promise",
        company=company.name
    )


async def send_delete_company_success_email(to: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на удаление учебного заведения с сайта Проекта Сфера",
        logo="logo.png",
        template="delete_company_success",
    )


async def send_delete_company_reject_email(to: str, company: _models.Company, reason: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на удаление учебного заведения с сайта Проекта Сфера",
        logo="logo.png",
        template="delete_company_success",
        company=company.name,
        reason=reason
    )


async def send_create_tags_promise_email(to: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на добавление новых тегов профессий на сайт Преокта Сфера",
        logo="logo.png",
        template="create_tags_promise"
    )


async def send_create_tags_success_email(to: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на добавление новых тегов профессий на сайт Преокта Сфера",
        logo="logo.png",
        template="create_tags_success",
        href=f"{_DOMAIN}/api/tags/all"
    )


async def send_create_tags_reject_email(to: str, reason: str):
    await _create_message(
        to=to,
        subject="Ответ по заявке на добавление новых тегов профессий на сайт Преокта Сфера",
        logo="logo.png",
        template="create_tags_reject",
        reason=reason
    )
