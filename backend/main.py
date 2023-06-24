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
from applications import applications as _applications
from staticpages import staticpages as _staticpages
from courses import courses as _courses


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
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "no user")
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
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


@fastapi.get("/api/companies/{id}", response_model=_schemas.Company)
async def get_company_public_data(
    id: int,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    return _services.get_company(id, session)


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
    if not user:
        return _cookies.get_unsign_response()
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
        return await _staticpages.get_link_invalid_page()
    except _links.LinkExpiredError:
        return await _staticpages.get_link_expired_page()
    except _links.LinkOverusedError:
        return await _staticpages.get_link_overused_page()
    except Exception as e:
        logger.error(f"Failed to process verification link {url}: {e}")
        return await _staticpages.get_link_500_error_page()
    else:
        return await _staticpages.get_verify_email_success_page()


@fastapi.get("/api/images/static/{name}")
async def get_logo_for_static_page(name: _schemas.static_logos):
    return _fastapi.responses.FileResponse(f"{_os.getcwd()}/data/logos/{name}")


@fastapi.post("/api/applications/company/create", status_code=204)
async def apply_for_company_registration(application: _schemas.CreateCompanyApplicationCreate):
    await _applications.add_create_company_application(application)


@fastapi.post("/api/applications/tags/create", status_code=204)
async def apply_for_tags_registration(application: _schemas.CreateTagApplicationCreate):
    await _applications.add_create_tags_application(application)


@fastapi.post("/api/applications/companies/{id}/update", status_code=204)
async def apply_for_company_update(
        id: int,
        application: _schemas.UpdateCompanyApplicationCreate,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    company = _services.get_company(id, session)
    await _applications.add_update_company_application(application, company)


@fastapi.post("/api/applications/companies/{id}/delete", status_code=204)
async def apply_for_company_deletion(
        id: int,
        application: _schemas.DeleteCompanyApplicationCreate,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    company = _services.get_company(id, session)
    await _applications.add_delete_company_application(application, company)


@fastapi.get("/api/applications/all", response_model=_schemas.AllApplications)
async def get_all_applications(
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        return _cookies.get_unsign_response()
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    return await _applications.get_all_applications()


@fastapi.put("/api/applications/{atype}/{id}", status_code=204)
async def respond_to_application(
    atype: _applications.applications_types,
    id: int,
    decision: _schemas.ApplicationDecision,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    if not user:
        return _cookies.get_unsign_response()
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()

    if atype == "create_company":
        application: _schemas.CreateCompanyApplication = await _applications.get_application(atype, id)
        if not application:
            raise _fastapi.HTTPException(404, "no such application")
        await _applications.delete_application(atype, id)
        if decision.apply:
            company = await _services.get_company_by_name(application.name, session)
            await _emails.send_create_company_success_email(application.applicant_email, company)
        else:
            await _emails.send_create_company_reject_email(application.applicant_email, decision.reason)
    elif atype == "create_tags":
        application: _schemas.CreateTagApplication = await _applications.get_application(atype, id)
        if not application:
            raise _fastapi.HTTPException(404, "no such application")
        await _applications.delete_application(atype, id)
        if decision.apply:
            await _emails.send_create_tags_success_email(application.applicant_email)
        else:
            await _emails.send_create_tags_reject_email(application.applicant_email, decision.reason)

    elif atype == "delete_company":
        application: _schemas.DeleteCompanyApplication = await _applications.get_application(atype, id)
        if not application:
            raise _fastapi.HTTPException(404, "no such application")
        await _applications.delete_application(atype, id)
        if decision.apply:
            await _emails.send_delete_company_success_email(application.applicant_email)
        else:
            await _emails.send_create_tags_reject_email(application.applicant_email, decision.reason)

    elif atype == "update_company":
        application: _schemas.UpdateCompanyApplication = await _applications.get_application(atype, id)
        if not application:
            raise _fastapi.HTTPException(404, "no such application")
        await _applications.delete_application(atype, id)
        company = await _services.get_company_by_name(application.name, session)
        if decision.apply:
            await _emails.send_update_company_success_email(application.applicant_email, company)
        else:
            await _emails.send_update_company_reject_email(application.applicant_email, company, decision.reason)


@fastapi.get("/api/tags/all", response_model=_typing.List[_schemas.Specialization])
async def get_all_tags(session: _orm.Session = _fastapi.Depends(_services.get_db_session)):
    return await _services.get_all_tags(session)


@fastapi.put("/api/companies/{id}", status_code=204)
async def update_company(
    id: int,
    update: _schemas.CompanyUpdate,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    if not user:
        return _cookies.get_unsign_response()
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    await _services.update_company(id, update, session)


@fastapi.delete("/api/companies/{id}", status_code=204)
async def delete_company(
    id: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    if not user:
        return _cookies.get_unsign_response()
    try:
        await _cookies.check_admin_cookie(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    await _services.drop_company(id, session)


@fastapi.get("/api/companies/all/", response_model=_typing.List[_schemas.Company])
async def get_all_companies(
    page: int = 1,
    pagesize: int = 20,
    desc: bool = False,
    sort: _schemas.companies_sort_types = "name",
    session: _orm.Session = _fastapi.Depends(_services.get_db_session),
    user: usertype = None,

):
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_all_companies(page-1, pagesize, sort, desc, session)


@fastapi.post("/api/courses/", status_code=204)
async def create_course(
        course: _schemas.CourseCreate,
        user: usertype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        usermodel = await _services.get_student_account(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    await _services.update_user_online(usermodel)
    course = await _services.create_course(course, session)
    _courses.initialize_course(course.id)


@fastapi.get("/api/courses/{id}", response_model=_schemas.Course)
async def get_course(
    id: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_course(id, session)


@fastapi.post("/api/courses/{id}/lessons", status_code=204)
async def create_course_lesson(
    id: int,
    data: _schemas.LessonCreate,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        usermodel = await _services.get_student_account(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if course.author_id != usermodel.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    lesson = await _services.create_lesson(course, data, session)
    _courses.initialize_lesson(course.id, lesson.number)


@fastapi.post("/api/courses/{id}/lessons/{number}/steps", response_model=int)
async def create_course_step(
    id: int,
    number: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        usermodel = await _services.get_student_account(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if course.author_id != usermodel.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _services.get_lesson(course, number)
    if not _courses.is_lesson_initialized(id, number):
        raise _fastapi.HTTPException(404, "no such lesson")
    return await _courses.initialize_step(id, number)


@fastapi.post("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/text", status_code=204)
async def set_step_text(
    id: int,
    lesson_number: int,
    step_number: int,
    text: _schemas.StepText,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        usermodel = await _services.get_student_account(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if course.author_id != usermodel.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _services.get_lesson(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    await _courses.write_into_step(id, lesson_number, step_number, text.text)


@fastapi.post("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/image", status_code=204)
async def load_step_image(
    id: int,
    lesson_number: int,
    step_number: int,
    upload: _fastapi.UploadFile,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    logger.debug("")
    if not user:
        raise _fastapi.HTTPException(401, "Нет cookie")
    try:
        usermodel = await _services.get_student_account(user, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if course.author_id != usermodel.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _services.get_lesson(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    await _courses.upload_step_image(id, lesson_number, step_number, upload)


@fastapi.get("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/text", response_model=str)
async def get_step_text(
    id: int,
    lesson_number: int,
    step_number: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.check_cookie_and_update_user_online(user, session)
    course = _services.get_course_model(id, session)
    await _services.get_lesson(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    return await _courses.get_step_text(id, lesson_number, step_number)


@fastapi.get("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/image")
async def get_step_image(
    id: int,
    lesson_number: int,
    step_number: int,
    user: usertype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.check_cookie_and_update_user_online(user, session)
    course = _services.get_course_model(id, session)
    await _services.get_lesson(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    return await _courses.get_step_image(id, lesson_number, step_number)
