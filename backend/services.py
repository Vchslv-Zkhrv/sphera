import typing as _typing

import fastapi as _fastapi
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from loguru import logger

import database as _database
import models as _models
import schemas as _schemas
from config import PASSWORD_SALT
import cookies as _cookies


def use_definition():
    return _database.Base.metadata.create_all(bind=_database.engine)


async def check_password(password: str, model: _models.signable,) -> bool:
    return hash.bcrypt.verify(password, model.password)


def get_db_session():
    se = _database.SessionLocal()
    try:
        yield se
    finally:
        se.close()


async def create_student(
        data: _schemas.StudentCreate,
        se: _orm.Session
):
    if se.query(_models.User).filter_by(email=data.email).all():
        raise _fastapi.HTTPException(400, "Почта занята")
    password = _hash.bcrypt.hash(data.password + PASSWORD_SALT)
    user = _models.User(
        fname=data.fname,
        lname=data.lname,
        sname=data.sname,
        email=data.email,
        password=password,
        role="student",
        online=True,
        date_created=_dt.datetime.utcnow(),
        date_online=_dt.datetime.utcnow(),
        sign=""
    )
    se.add(user)
    se.commit()
    se.refresh(user)
    return user


def update_user_online(
        user: _models.User,
        se: _orm.Session
):
    user.date_online = _dt.datetime.now()
    se.commit()
    se.refresh(user)
    return user


async def get_student_account(
        cookie: str,
        se: _orm.Session
):
    stud = await _cookies.check_user_cookie(cookie, se)
    update_user_online(stud, se)
    return stud


async def get_teacher_account(
        cookie: str,
        se: _orm.Session
):
    user = await _cookies.check_user_cookie(cookie, se)
    update_user_online(user, se)
    teacher = se.get(_models.Teacher, user.id)
    teacher.specializations