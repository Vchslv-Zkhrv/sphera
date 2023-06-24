import typing as _typing

import fastapi as _fastapi
import datetime as _dt
import sqlalchemy.orm as _orm
from sqlalchemy import func as _func
import passlib.hash as _hash
import pydantic as _pydantic
from loguru import logger as _logger

import database as _database
import models as _models
import schemas as _schemas
from config import PASSWORD_SALT
import cookies as _cookies


"""
Работа с базой данных

"""


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
    if not user.confirmed:
        raise _fastapi.HTTPException(409, "email not verified")
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
        company_id=company.id,
        bio=data.bio
    )
    se.add(teacher)
    se.commit()
    se.refresh(teacher)

    for s in specializations:
        se.add(
            _models.TeacherSpecializations(
                user_id=teacher.user_id,
                specialization_id=s.id
            )
        )
        se.commit()

    return (user, teacher)


def get_teacher(
        user_id: int,
        se: _orm.Session
):
    teacher = se.get(_models.Teacher, user_id)
    if not teacher:
        raise _fastapi.HTTPException(400, "User is not a teacher")
    if not teacher.user.confirmed:
        raise _fastapi.HTTPException(409, "email is not verified")
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
        raise _cookies.CookieError
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


def get_company(
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
        tags=list(s.specialization.name for s in model.specializations),
        contacts=list(_schemas.CompanyContact.from_orm(c) for c in model.contacts)
    )


async def get_company_by_name(
       name: str,
       se: _orm.Session 
):
    model = se.query(_models.Company).filter_by(name=name).first()
    if not model:
        raise _fastapi.HTTPException(404, "no such company")
    return _schemas.Company(
        id=model.id,
        name=model.name,
        teachers=model.teachers,
        tags=list(s.specialization.name for s in model.specializations),
        contacts=list(_schemas.CompanyContact.from_orm(c) for c in model.contacts)
    )


def teacher_model_to_schema(
        user: _models.User,
        teacher: _models.Teacher
):
    return _schemas.Teacher(
        id=user.id,
        email=user.email,
        fname=user.fname,
        lname=user.lname,
        sname=user.sname,
        date_online=user.date_online,
        company=teacher.company.name,
        specializations=list(
            s.specialization.name for s in teacher.specializations
        )
    )


async def get_all_students(se: _orm.Session):
    return list(
        _schemas.StudentShort.from_orm(s)
        for s in
        se.query(_models.User).filter_by(role="student")
    )


async def get_all_teachers(se: _orm.Session):
    return list(
        _schemas.TeacherShort(
            id=teacher.user_id,
            fname=teacher.user.fname,
            lname=teacher.user.lname,
            sname=teacher.user.sname,
            company=teacher.company_name
        )
        for teacher in
        se.query(_models.Teacher)
    )


async def get_student_by_id(
        id: int,
        se: _orm.Session
):
    model = se.query(_models.User).filter_by(id=id).filter_by(role="student").first()
    if not model:
        raise _fastapi.HTTPException(404, "No such user")
    return _schemas.StudentFull(
        id=model.id,
        email=model.email,
        fname=model.fname,
        lname=model.lname,
        sname=model.sname,
        date_online=model.date_online,
        activities=list(a.date for a in model.activities)
    )


async def drop_student_by_id(
        id: int,
        se: _orm.Session
):
    user = se.query(_models.User).filter_by(id=id).filter_by(role="student").first()
    if not user:
        raise _fastapi.HTTPException(404, "No such user")
    se.delete(user)
    se.commit()


async def get_teacher_by_id(
        id: int,
        se: _orm.Session
):
    teacher = se.get(_models.Teacher, id)
    if not teacher:
        raise _fastapi.HTTPException(404, "No such teacher")
    return _schemas.TeacherFull(
        id=teacher.user.id,
        email=teacher.user.email,
        fname=teacher.user.fname,
        lname=teacher.user.lname,
        sname=teacher.user.sname,
        date_online=teacher.user.date_online,
        company=teacher.company.name,
        specializations=list(s.specialization.name for s in teacher.specializations),
        activities=list(a.date for a in teacher.user.activities)
    )


async def drop_teacher_by_id(
        id: int,
        se: _orm.Session
):
    teacher = se.get(_models.Teacher, id)
    se.delete(teacher)
    se.commit()


async def create_company(
        data: _schemas.CompanyCreate,
        se: _orm.Session
):
    if se.query(_models.Company).filter_by(name=data.name).first():
        raise _fastapi.HTTPException(400, "Company already exists")

    for tag in data.tags:
        if not se.query(_models.Specialization).filter_by(name=tag).first():
            raise _fastapi.HTTPException(404, f"no such tag: {tag}")

    company = _models.Company(name=data.name)
    se.add(company)
    se.commit()
    se.refresh(company)
    if not company:
        raise _fastapi.HTTPException(409, "Unable to save company")

    for tag in data.tags:
        tag_model = se.query(_models.Specialization).filter_by(name=tag).first()
        cp = _models.CompanySpecializations(
            company_id=company.id,
            specialization_id=tag_model.id
        )
        se.add(cp)
        se.commit()

    for contact in data.contacts:
        model = _models.CompanyContacts(
            company_id=company.id,
            kind=contact.kind,
            value=contact.value
        )
        se.add(model)
        se.commit()


async def get_all_tags(se: _orm.Session):
    return _pydantic.parse_obj_as(
        _typing.List[_schemas.Specialization],
        se.query(_models.Specialization).all()
    )


async def update_company(
        id: int,
        update: _schemas.CompanyUpdate,
        se: _orm.Session
):
    company = se.get(_models.Company, id)
    if not company:
        raise _fastapi.HTTPException(404, "No such company")
    if update.name:
        company.name = update.name
        se.commit()
        se.refresh(company)
    if update.contacts:
        for oldc in company.contacts:
            se.delete(oldc)
            se.commit()
        for new in update.contacts:
            se.add(_models.CompanyContacts(kind=new.kind, value=new.value, company_id=company.id))
            se.commit()
    if update.tags:
        new = list(se.query(_models.Specialization).filter_by(name=tag).first() for tag in update.tags)
        if None in new:
            raise _fastapi.HTTPException(404, "No such tag")
        for olds in company.specializations:
            se.delete(olds)
            se.commit()
        for n in new:
            se.add(_models.CompanySpecializations(company_id=company.id, specialization_id=n.id))
            se.commit()


async def drop_company(
        id: int,
        se: _orm.Session
):
    company = se.get(_models.Company, id)
    if not company:
        raise _fastapi.HTTPException(404, "No such company")
    if len(company.teachers) > 0:
        raise _fastapi.HTTPException(409, "Unable delete an organization that has registered teachers")
    for tag in company.specializations:
        se.delete(tag)
        se.commit()
    for contact in company.contacts:
        se.delete(contact)
        se.commit()
    se.delete(company)
    se.commit()


async def get_all_companies(
        page: int,
        pagesize: int,
        sort: _schemas.companies_sort_types,
        desc: bool,
        se: _orm.Session
):
    sort_column = _models.Company.id if sort == "id" else _models.Company.name
    sort_column = sort_column.desc() if desc else sort_column
    return list(
        get_company(company.id, se)
        for company in
        (
            se
            .query(_models.Company)
            .order_by(sort_column)
            .offset(page*pagesize)
            .limit(pagesize)
        )
    )


async def create_course(
        data: _schemas.CourseCreate,
        se: _orm.Session
):
    if se.query(_models.Course).filter_by(name=data.name).first():
        raise _fastapi.HTTPException(409, "Course name already in use")
    tags = list(se.query(_models.Specialization).filter_by(name=tname).first() for tname in data.tags)
    if None in tags:
        raise _fastapi.HTTPException(404, "No such tag")
    course = _models.Course(
        author_id=data.author_id,
        name=data.name,
        description=data.description,
        date_created=_dt.datetime.utcnow(),
        date_updated=_dt.datetime.utcnow(),
        views=0
    )
    se.add(course)
    se.commit()
    se.refresh(course)
    for tag in tags:
        se.add(_models.CourseTags(
            specialization_id=tag.id,
            course_id=course.id
        ))
        se.commit()
    se.refresh(course)
    return course


async def create_lesson(
        course: _models.Course,
        data: _schemas.LessonCreate,
        se: _orm.Session
):
    lesson = _models.Lesson(
        name=data.name,
        duration=data.duration,
        description=data.description,
        course_id=course.id,
        number=data.number
    )
    se.add(lesson)
    se.commit()
    se.refresh(lesson)
    return lesson


def get_course_model(
        id: int,
        se: _orm.Session
):
    course = se.get(_models.Course, id)
    if not course:
        raise _fastapi.HTTPException(404, "No such course")
    course.views += 1
    se.commit()
    se.refresh(course)
    return course


async def get_course(
        id: int,
        se: _orm.Session
):
    course = get_course_model(id, se)
    if course.author.role == "teacher":
        author = _schemas.TeacherShort(
            id=course.author.id,
            fname=course.author.fname,
            lname=course.author.lname,
            sname=course.author.sname,
            company=course.author.teacher.company.name
        )
    else:
        author = _schemas.StudentShort.from_orm(course.author)
    return _schemas.Course(
        id=id,
        name=course.name,
        description=course.description,
        author=author,
        date_created=course.date_created,
        date_updated=course.date_updated,
        views=course.views,
        tags=list(_schemas.Specialization.from_orm(t.specialization) for t in course.tags),
        lessons=_pydantic.parse_obj_as(_typing.List[_schemas.LessonShort], course.lessons),
    )


async def check_cookie_and_update_user_online(
        cookie: str,
        se: _orm.Session
):
    if not cookie:
        return
    try:
        user = await get_student_account(cookie, se)
        user.date_online = _dt.datetime.utcnow()
        se.commit()
        se.refresh(user)
    except _cookies.CookieError:
        return
    except Exception as e:
        _logger.error(f"cannot update user date online {e=}")


async def get_lesson(
        course: _models.Course,
        number: int
):
    for lesson in course.lessons:
        if number==lesson.number:
            return lesson
    else:
        raise _fastapi.HTTPException(404, "No such lesson")
