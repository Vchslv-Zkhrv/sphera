import typing as _typing
import datetime as _dt
import hashlib as _hash
import random as _rand

import fastapi as _fastapi
from sqlalchemy import orm as _orm
from pydantic import BaseModel as _BM

import models as _models
import database as _database


class CookieError(Exception):
    pass


class InvalidSignError(CookieError):
    pass


class InvalidCookieEror(CookieError):
    pass


async def genetate_cookie(
        model: _models.signable,
        db: _orm.Session
):

    """
    Создает случайную подпись для куки и сохраняет ее в базе данных.
    Вовзращает новое значение куки.
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


async def get_signed_response(
        data: _typing.Optional[_BM],
        model: _models.signable,
        se: _orm.Session,
        status: int = 200,
        path: str = "/"
):

    """
    Создает новую подпись куки и формирует http-запрос
    """

    resp = _fastapi.Response(data.json() if data else None, media_type="application/json")
    cookie = await genetate_cookie(model, se)
    resp.set_cookie("user", cookie, httponly=True, path=path)
    resp.status_code = status
    return resp


def get_unsign_response(status: int = 401, path: str = "/"):
    resp = _fastapi.Response(status_code=status)
    resp.delete_cookie("user", path=path)
    return resp
