import typing as _typing

import smtplib as _smtplib
import ssl as _ssl
from email.mime.text import MIMEText as _MIMEText
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from loguru import logger


from ..config import SMTP_LOGIN, SMTP_APPLICATION_PASSWORD


def send(
        subject: str,
        to: _typing.List[str],
        message: str
):
    logger.debug("new message")
    context = _ssl.create_default_context()
    try:
        with _smtplib.SMTP_SSL("smtp.yandex.ru", 465, timeout=5, context=context) as server:
            server.ehlo()
            server.login(SMTP_LOGIN, SMTP_APPLICATION_PASSWORD)
            server.sendmail(SMTP_LOGIN, to, message)
    except Exception as e:
        logger.error(f"an exception occurred while sending the message: {e}")
