import os as _os
import typing as _typing

import fastapi as _fastapi
from sqlalchemy import orm as _orm
from loguru import logger

import cookies as _cookies
import services as _services
import schemas as _schemas
from emails import emails as _emails
import links as _links


"""
Точка входа в приложение. Принимает HTTP-запросы и отдает HTTP-ответы

"""


fastapi = _fastapi.FastAPI()

usertype = _typing.Annotated[_typing.Union[str, None], _fastapi.Cookie()]

logger.add("./logs/debug.log")


@fastapi.head("/api/", status_code=204)
async def handshake():
    pass


@fastapi.post("/app/students", status_code=204)
async def student_sign_up(
    data: _schemas.StudentCreate,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    user = await _services.create_student(data, session)
    link = await _links.create_verify_email_link(user, session)
    await _emails.send_verification_email(link, user)


@fastapi.get("/app/students/me", response_model=_schemas.Student)
async def student_sign_in(
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
async def student_auth(
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
    logger.debug("")
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
    return await _cookies.get_signed_response(schema, model, session)


@fastapi.delete("/api/admin", status_code=401)
async def admin_log_out():
    logger.debug("")
    return _cookies.get_unsign_response()


@fastapi.post("/api/tags",  status_code=204)
async def load_tags(
    tags: _typing.List[str],
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    await _services.create_specializations(tags, session)


@fastapi.get("/api/tags", response_model=_typing.List[_schemas.Specialization])
async def find_tags(
    pattern: str,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
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
    logger.debug("")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response("/api/admin")
    await _services.create_company(data, session)


@fastapi.get("/api/compamies/{id}", response_model=_schemas.Company)
async def get_company_public_data(
    id: int,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    return await _services.get_company(id, session)


@fastapi.post("/app/teachers", status_code=204)
async def teacher_sign_up(
    data: _schemas.TeacherCreate,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    usr, _ = await _services.create_teacher(data, session)
    await _cookies.get_signed_response(None, usr, session, 204)


@fastapi.get("/app/teachers/me", response_model=_schemas.Teacher)
async def teacher_sign_in(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        usr, teacher = await _services.get_teacher_account(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    data = _services.teacher_model_to_schema(usr, teacher)
    return await _cookies.get_signed_response(data, usr, session)


@fastapi.get("/api/admin/students/all", response_model=_typing.List[_schemas.StudentShort])
async def get_all_students(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    return await _services.get_all_students(session)


@fastapi.get("/api/admin/teachers/all", response_model=_typing.List[_schemas.TeacherShort])
async def get_all_teachers(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    return await _services.get_all_teachers(session)


@fastapi.delete("/api/admin/students/{id}", status_code=204)
async def delete_student_by_admin(
    id: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    await _services.drop_student_by_id(id, session)


@fastapi.delete("/api/admin/teachers/{id}", status_code=204)
async def delete_teachers_by_admin(
    id: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    model = await _services.get_student_by_id(id, session)
    if not model:
        raise _fastapi.HTTPException(404, "No such user")
    session.delete(model)
    session.commit()


@fastapi.get("/api/admin/teachers/{id}", response_model=_schemas.TeacherFull)
async def get_teacher_by_admin(
    id: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    return await _services.get_teacher_by_id(id, session)


@fastapi.get("/api/admin/student/{id}", response_model=_schemas.StudentFull)
async def get_student_by_admin(
    id: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    return await _services.get_student_by_id(id, session)


@fastapi.get("/api/verification/{url}", status_code=200)
async def email_verification(
    url: str,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug(f"new link: {url}")
    try:
        await _links.verify_email(url, session)
    except _links.LinkInvalidError:
        return await _emails.get_link_invalid_page()
    except _links.LinkExpiredError:
        return await _emails.get_link_expired_page()
    except _links.LinkOverusedError:
        return await _emails.get_link_overused_page()
    except Exception as e:
        logger.error(f"Failed to process verification link {url}: {e}")
        return await _emails.get_link_500_error_page()
    else:
        return await _emails.get_verify_email_success_page()


@fastapi.get("/api/images/email/")
async def get_logo_for_email():
    return _fastapi.responses.FileResponse(f"{_os.getcwd()}/emails/media/logo.png")


@fastapi.get("/api/images/static/{name}")
async def get_logo_for_static_page(name:_emails.static_logos):
    return _fastapi.responses.FileResponse(f"{_os.getcwd()}/emails/media/{name}")
