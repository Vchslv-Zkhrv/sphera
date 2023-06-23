import datetime as _datetime
import hashlib as _hashlib

import fastapi as _fastapi
from sqlalchemy import orm as _orm

import models as _models
import schemas as _schemas


"""
Работа с ссылками на выполнение действий

"""


async def create_verify_email_link(
        user: _models.User,
        se: _orm.Session
):
    url = _hashlib.sha1(str(_datetime.datetime.now().timestamp()).encode()).hexdigest()
    link = _models.Link(
        url=url,
        limit=1,
        target=user.id,
        action="verify email",
        date_expired=_datetime.datetime.now() + _datetime.timedelta(hours=1)
    )
    se.add(link)
    se.commit()
    return link


def get_link_by_url(
        url: str,
        se: _orm.Session
):
    link = se.query(_models.Link).filter_by(url=url).first()
    if not link:
        raise _fastapi.HTTPException(400, "Неверная ссылка")
    schema = _schemas.Link.from_orm(link)
    if link.limit <= link.count_used:
        se.delete(link)
        se.commit()
        raise _fastapi.HTTPException(400, "Превышено ограничение на использование ссылки")
    if schema.date_expired < _datetime.datetime.now():
        se.delete(link)
        se.commit()
        raise _fastapi.HTTPException(400, "Ссылка устарела")
    return link


async def verify_email(
        url: str,
        se: _orm.Session
):
    link = get_link_by_url(url, se)
    user = se.get(_models.User, link.target)
    if not user:
        raise _fastapi.HTTPException(404, "No such user")
    user.confirmed = True
    link.count_used += 1
    se.commit()
    se.refresh(user)
