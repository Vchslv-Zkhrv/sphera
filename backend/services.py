import typing as _typing

import fastapi as _fastapi
import datetime as _dt
import sqlalchemy.orm as _orm
from sqlalchemy import func as _func
import passlib.hash as _hash

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


async def auth_student(
        login: str,
        password: str,
        se: _orm.Session
):
    user = se.query(_models.User).filter_by(email=login).first()
    if not user:
        raise _fastapi.HTTPException(404, "No such user")
    if not _hash.bcrypt.hash(password + PASSWORD_SALT):
        raise _fastapi.HTTPException(401, "invalid password")
    return user


async def get_student_account(
        cookie: str,
        se: _orm.Session
):
    stud = await _cookies.check_user_cookie(cookie, se)
    update_user_online(stud, se)
    return stud


async def drop_student(
        cookie: str,
        se: _orm.Session
):
    stud = await _cookies.check_user_cookie(cookie, se)
    se.delete(stud)
    se.commit()


async def update_student(
    data: _schemas.StudentUpdate,
    model: _models.User,
    se: _orm.Session
):
    if data.email:
        model.email = data.email
        se.commit()
        se.refresh(model)
    if data.fname:
        model.fname = data.fname
        se.commit()
        se.refresh(model)
    if data.sname:
        model.sname = data.sname
        se.commit()
        se.refresh(model)
    if data.lname:
        model.lname = data.lname
        se.commit()
        se.refresh(model)
    if data.password:
        model.password = _hash.bcrypt.hash(data.password + PASSWORD_SALT)
        se.commit()
        se.refresh(model)


async def create_teacher(
        data: _schemas.TeacherCreate,
        se: _orm.Session
):
    if se.query(_models.User).filter_by(email=data.email).all():
        raise _fastapi.HTTPException(400, "Почта занята")

    company = se.get(_models.Company, data.company)
    if not company:
        raise _fastapi.HTTPException(404, "Компания не найдена")

    specializations = list(
        se
        .query(_models.Specialization)
        .filter_by(name=sp)
        .first()
        for sp in data.specializations
    )
    if None in specializations:
        raise _fastapi.HTTPException(404, "Не найдена специализация")

    password = _hash.bcrypt.hash(data.password + PASSWORD_SALT)
    user = _models.User(
        fname=data.fname,
        lname=data.lname,
        sname=data.sname,
        email=data.email,
        password=password,
        role="teacher",
        date_created=_dt.datetime.utcnow(),
        date_online=_dt.datetime.utcnow(),
        sign=""
    )
    se.add(user)
    se.commit()
    se.refresh(user)

    teacher = _models.Teacher(
        user_id=user.id,
        company_name=company.name,
        bio=data.bio
    )
    se.add(teacher)
    se.commit()
    se.refresh(teacher)

    teacher.specializations = specializations
    se.commit()
    return (user, teacher)


def get_teacher(
        user_id: int,
        se: _orm.Session
):
    teacher = se.get(_models.Teacher, user_id)
    if not teacher:
        raise _fastapi.HTTPException(400, "User is not a teacher")
    else:
        return teacher


async def auth_teacher(
        login: str,
        password: str,
        se: _orm.Session
):
    user = se.query(_models.User).filter_by(email=login).first()
    if not user:
        raise _fastapi.HTTPException(404, "No such user")
    if not _hash.bcrypt.hash(password + PASSWORD_SALT):
        raise _fastapi.HTTPException(401, "invalid password")
    teacher = get_teacher(user.id, se)
    return (user, teacher)


async def get_teacher_account(
        cookie: str,
        se: _orm.Session
):
    user = await _cookies.check_user_cookie(cookie, se)
    update_user_online(user, se)
    teacher = get_teacher(user.id, se)
    return (user, teacher)


async def drop_teacher(
        cookie: str,
        se: _orm.Session
):
    user = await _cookies.check_user_cookie(cookie, se)
    teacher = get_teacher(user.id, se)
    se.delete(teacher)
    se.commit()
    se.delete(user)
    se.commit()


async def update_teacher(
    data: _schemas.TeacherUpdate,
    user: _models.User,
    teacher: _models.Teacher,
    se: _orm.Session
):
    if data.email:
        user.email = data.email
        se.commit()
        se.refresh(user)
    if data.fname:
        user.fname = data.fname
        se.commit()
        se.refresh(user)
    if data.sname:
        user.sname = data.sname
        se.commit()
        se.refresh(user)
    if data.lname:
        user.lname = data.lname
        se.commit()
        se.refresh(user)
    if data.password:
        user.password = _hash.bcrypt.hash(data.password + PASSWORD_SALT)
        se.commit()
        se.refresh(user)
    if data.company:
        company = se.get(_models.Company, data.company)
        if company:
            teacher.company = company
        se.commit()
        se.refresh(teacher)
    if data.specializations:
        specializations = list(
            filter(
                se
                .query(_models.Specialization)
                .filter_by(name=sp)
                .first()
                for sp in data.specializations
            )
        )
        teacher.specializations = specializations
        se.commit()
        se.refresh(teacher)


async def auth_admin(
        login: str,
        password: str,
        se: _orm.Session
):
    admin = (
        se
        .query(_models.Admin)
        .filter_by(login=login)
        .first()
    )
    if not admin:
        raise _fastapi.HTTPException(404, "No such admin")
    if not _hash.bcrypt.verify(password+PASSWORD_SALT, admin.password):
        raise _fastapi.HTTPException(401, "Invalid credentials")
    return admin


async def drop_admin(
        cookie: str,
        se: _orm.Session
):
    admin = await _cookies.check_admin_cookie(cookie, se)
    se.delete(admin)
    se.commit()


async def create_specializations(
        names: _typing.List[str],
        se: _orm.Session
):
    for name in names:
        if se.query(_models.Specialization).filter_by(name=name).first():
            continue
        spec = _models.Specialization(name=name)
        se.add(spec)
        se.commit()


async def find_specializations(
        pattern: str,
        se: _orm.Session
):

    return (
        se
        .query(_models.Specialization)
        .filter(_func.lower(_models.Specialization.name).like(f"%{pattern}%"))
        .all()
    )


async def create_company(
        data: _schemas.CompanyCreate,
        se: _orm.Session
):
    comp = _models.Company(name=data.name)
    se.add(comp)
    se.commit()
    se.refresh(comp)
    specs = list(
        se
        .query(_models.Specialization)
        .filter_by(name=s)
        .first()
        for s in
        data.tags
    )
    specs = list(
        _models.CompanySpecializations(
            company_id=comp.id,
            specialization_id=s.id
        )
        for s in specs
    )
    for s in specs:
        se.add(s)
        se.commit()


async def get_company(
        id: int,
        se: _orm.Session
):
    model = se.get(_models.Company, id)
    if not model:
        raise _fastapi.HTTPException(404, "no such company")
    return _schemas.Company(
        id=id,
        name=model.name,
        teachers=model.teachers,
        tags=list(s.specialization.name for s in model.specializations)
    )
