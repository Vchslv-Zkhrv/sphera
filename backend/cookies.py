import typing as _typing

import datetime as _dt
import hashlib as _hash
import random as _rand

from sqlalchemy import orm as _orm

import models as _models
import database as _database

class InvalidSignError(Exception):
    pass


class InvalidCookieEror(Exception):
    pass


async def genetate_cookie(
        model: _database.Base,
        db: _orm.Session
):

    """
    Создает случайную подпись для куки и сохраняет ее в базе данных.
    Вовзращает новое значение куки.
    Должна использоваться при каждом запросе
    """

    timestamp = str(_dt.datetime.now().timestamp()+_rand.randint(0, 99999999))
    sign = _hash.sha256(timestamp.encode()).hexdigest()
    model.sign = sign
    db.commit()
    return f"{model.id}.{sign}"


async def check_cookie(
        cookie: str,
        model: _typing.Type[_database.Base],
        db: _orm.Session
):

    """
    Проверяет цифровую подпись куки и, если все в порядке, возвращает модель пользователя
    """

    try:
        values = cookie.split(".")
        uid = int(values[0])
        sign = values[1]
    except (TypeError, ValueError, KeyError):
        raise InvalidCookieEror

    user = db.get(model, uid)

    if user.sign != sign or user.id != uid:
        raise InvalidSignError

    return user


async def check_user_cookie(
        cookie: str,
        db: _orm.Session
) -> _models.User:
    return await check_cookie(cookie, _models.User, db)


async def check_admin_cookie(
        cookie: str,
        db: _orm.Session
) -> _models.Admin:
    return await check_cookie(cookie, _models.Admin, db)
