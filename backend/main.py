import typing as _typing

import fastapi as _fastapi
from sqlalchemy import orm as _orm
from loguru import logger

import cookies as _cookies
import services as _services
import schemas as _schemas
import models as _models


fastapi = _fastapi.FastAPI()

usertype = _typing.Annotated[_typing.Union[str, None], _fastapi.Cookie()]

logger.add("./logs/debug.log")


@fastapi.post("/app/students", status_code=204)
async def student_sign_up(
    data: _schemas.StudentCreate,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    stud = await _services.create_student(data, session)
    return await _cookies.get_signed_response(None, stud, session, 204)


@fastapi.get("/app/students/me/cookie", response_model=_schemas.Student)
async def student_cookie_sign_in(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        student = await _services.get_student_account(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    data = _schemas.Student.from_orm(student)
    return await _cookies.get_signed_response(data, student, session)


@fastapi.post("/api/students/me", response_model=_schemas.Student)
async def student_sign_in(
    data: _schemas.AuthSchema,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    usr = await _services.auth_student(data.login, data.password, session)
    stud = _schemas.Student.from_orm(usr)
    return await _cookies.get_signed_response(stud, usr, session)


@fastapi.delete("/app/students/me/cookie", status_code=401)
async def student_logout():
    logger.debug("")
    resp = _fastapi.Response(status_code=401)
    resp.delete_cookie("user")
    return resp


@fastapi.delete("/api/students/me", status_code=204)
async def delete_student_account(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    try:
        await _services.drop_student(user, session)
    finally:
        return _cookies.get_unsign_response()


@fastapi.put("/api/students/me", status_code=204)
async def update_student_data(
    data: _schemas.StudentUpdate,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    try:
        _cookies.check_user_cookie(user, session)
        model = await _services.auth_student(data.confirmation_email, data.confirmation_password, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()

    await _services.update_student(data, model, session)
    return await _cookies.get_signed_response(None, model, session, 204)


@fastapi.get("/api/admin", response_model=_schemas.Admin)
async def admin_sign_in(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    if not user:
        raise _fastapi.HTTPException(401, "no user")
    try:
        model = await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    schema = _schemas.Admin.from_orm(model)
    return await _cookies.get_signed_response(
        schema,
        model,
        session,
    )


@fastapi.post("/api/admin", response_model=_schemas.Admin)
async def admin_auth(
        data: _schemas.AuthSchema,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    try:
        model = await _services.auth_admin(data.login, data.password, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    schema = _schemas.Admin.from_orm(model)
    return await _cookies.get_signed_response(
        schema,
        model,
    )


@fastapi.delete("/api/admin", status_code=401)
async def admin_log_out(
    user: usertype = None,
):
    return _cookies.get_unsign_response()


@fastapi.post("/api/tags",  status_code=204)
async def load_tags(
    tags: _typing.List[str],
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.create_specializations(tags, session)


@fastapi.get("/api/tags", response_model=_typing.List[_schemas.Specialization])
async def find_tags(
    pattern: str,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    return list(
        _schemas.Specialization.from_orm(s)
        for s in
        await _services.find_specializations(pattern, session)
    )


@fastapi.post("/api/companies", status_code=204)
async def regist_company(
    data: _schemas.CompanyCreate,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):

    if not user:
        raise _fastapi.HTTPException(401, "no cookie")

    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        try:
            await _cookies.check_user_cookie(user, session)
        except _cookies.CookieError:
            return _cookies.get_unsign_response("/api/admin")

    await _services.create_company(data, session)


@fastapi.get("/api/compamies/{id}", response_model=_schemas.Company)
async def get_company_public_data(
    id: int,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    return await _services.get_company(id, session)
