import typing as _typing
import datetime as _dt

import fastapi as _fastapi
from sqlalchemy import orm as _orm

import cookies as _cookies
import services as _services
import schemas as _schemas


fastapi = _fastapi.FastAPI()

usertype = _typing.Annotated[_typing.Union[str, None], _fastapi.Cookie()]


@fastapi.post("/app/students", status_code=204)
async def user_signup(
    data: _schemas.StudentCreate,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    stud = await _services.create_student(data, session)
    return await _cookies.get_signed_response(None, stud, session)


@fastapi.get("/app/students/me/cookie", response_model=_schemas.Student)
async def get_student_account(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        student = await _services.get_student_account(user, session)
    except _cookies.CookieError:
        resp = _fastapi.Response(status_code=401)
        resp.delete_cookie("user")
        return resp
    data = _schemas.Student.from_orm(student)
    return await _cookies.get_signed_response(data, student, session)


@fastapi.delete("/app/students/me/cookie", status_code=401)
async def user_logout():
    resp = _fastapi.Response(status_code=401)
    resp.delete_cookie("user")
    return resp
