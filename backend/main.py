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
from news import news as _news

"""
Точка входа в приложение. Принимает HTTP-запросы и отдает HTTP-ответы

"""


fastapi = _fastapi.FastAPI()

cookietype = _typing.Annotated[_typing.Union[str, None], _fastapi.Cookie()]

logger.add("./logs/debug.log", rotation="1MB")


@fastapi.head("/api/", status_code=204)
async def handshake():
    """ Проверка соединения """
    pass


@fastapi.post("/api/students", status_code=204)
async def student_sign_up(
    data: _schemas.StudentCreate,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Регистрация нового студента """
    logger.debug("")
    user = await _services.create_student(data, session)
    link = await _links.create_verify_email_link(user, session)
    await _emails.send_verification_email(link, user)


@fastapi.get("/api/users/me", response_model=_typing.Union[_schemas.Student, _schemas.Teacher])
async def user_sign_in(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Вход в аккаунт любого пользователя по cookie """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role not in ("student", "teacher") or not model:
        return _cookies.get_unsign_response()
    if role == "student":
        data = _schemas.Student.from_orm(model)
        return await _cookies.get_signed_response(data, model, session)
    elif role == "teacher":
        data = _services.teacher_model_to_schema(model.user, model)
        return await _cookies.get_signed_response(data, model.user, session)


@fastapi.get("/api/students/me", response_model=_schemas.Student)
async def student_sign_in(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Вход в аккаунт студента по cookie """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "student" or not model:
        return _cookies.get_unsign_response()
    data = _schemas.Student.from_orm(model)
    return await _cookies.get_signed_response(data, model, session)


@fastapi.post("/api/students/me", response_model=_schemas.Student)
async def student_auth(
    data: _schemas.AuthSchema,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Вход в аккаунт студента по логину и паролю """
    logger.debug("")
    usr = await _services.auth_student(data.login, data.password, session)
    stud = _schemas.Student.from_orm(usr)
    return await _cookies.get_signed_response(stud, usr, session)


@fastapi.delete("/api/users/me/cookie", status_code=401)
async def user_logout():
    """ Выход из аккаунта пользователя """
    logger.debug("")
    resp = _fastapi.Response(status_code=401)
    resp.delete_cookie("user")
    return resp


@fastapi.delete("/api/students/me", status_code=204)
async def delete_student_account(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Удаление аккаунта студента """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "student":
        return _cookies.get_unsign_response()
    await _services.drop_student(model, session)
    return _cookies.get_unsign_response(204)


@fastapi.put("/api/students/me", status_code=204)
async def update_student_data(
    data: _schemas.StudentUpdate,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Изменение данных аккаунта студента.
    Доступно только для владельца аккаунта
    """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "student":
        return _cookies.get_unsign_response()
    await _services.update_student(data, model, session)
    return await _cookies.get_signed_response(None, model, session, 204)


@fastapi.get("/api/admin", response_model=_schemas.Admin)
async def admin_sign_in(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Вход по cookie для админа """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "admin":
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
    """ Вход в аккаунт админа по логину и паролю """
    logger.debug("")
    try:
        model = await _services.auth_admin(data.login, data.password, session)
    except _cookies.CookieError:
        return _cookies.get_unsign_response()
    schema = _schemas.Admin.from_orm(model)
    return await _cookies.get_signed_response(schema, model, session)


@fastapi.delete("/api/admin", status_code=401)
async def admin_log_out():
    """ Выход из аккаунта админа """
    logger.debug("")
    return _cookies.get_unsign_response()


@fastapi.post("/api/tags",  status_code=204)
async def load_tags(
    tags: _typing.List[str],
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Добавление тегов профессий на сайт.
    Доступно только для админов
    """
    logger.debug("")
    _, role = await _services.get_account_by_cookie(user, session)
    if role != "admin":
        return _cookies.get_unsign_response()
    await _services.create_specializations(tags, session)


@fastapi.get("/api/tags", response_model=_typing.List[_schemas.Specialization])
async def find_tags(
    pattern: str,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Поиск тегов по шаблону """
    logger.debug("")
    return list(
        _schemas.Specialization.from_orm(s)
        for s in
        await _services.find_specializations(pattern, session)
    )


@fastapi.post("/api/companies", status_code=204)
async def regist_company(
    data: _schemas.CompanyCreate,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Регистрация учебной огранизации.
    Доступно только для админов
    """
    logger.debug("")
    _, role = await _services.get_account_by_cookie(user, session)
    if role != "admin":
        return _cookies.get_unsign_response()
    await _services.create_company(data, session)


@fastapi.get("/api/companies/{id}", response_model=_schemas.Company)
async def get_company(
    id: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получение странички учебной организации """
    logger.debug("")
    await _services.check_cookie_and_update_user_online(user, session)
    return _services.get_company(id, session)


@fastapi.post("/api/teachers", status_code=204)
async def teacher_sign_up(
    data: _schemas.TeacherCreate,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Регистрация аккаунта учителя """
    logger.debug("")
    user, _ = await _services.create_teacher(data, session)
    link = await _links.create_verify_email_link(user, session)
    await _emails.send_verification_email(link, user)


@fastapi.get("/api/teachers/me", response_model=_schemas.Teacher)
async def teacher_sign_in(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Вход в аккаунт учителя по cookie """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "teacher" or not model:
        return _cookies.get_unsign_response()
    data = _services.teacher_model_to_schema(model.user, model)
    return await _cookies.get_signed_response(data, model.user, session)


@fastapi.put("/api/teachers/me", status_code=204)
async def update_teacher(
    update: _schemas.TeacherUpdate,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Редактирование аккаунта учителя """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "teacher":
        return _cookies.get_unsign_response()
    await _services.update_teacher(update, model.user, model, session)


@fastapi.delete("/api/teachers/me", status_code=204)
async def delete_teacher_account(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Удаление аккаунта учителя """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "teacher":
        return _cookies.get_unsign_response()
    await _services.drop_teacher(model, session)
    _cookies.get_unsign_response(204)


@fastapi.get("/api/admin/students/all", response_model=_typing.List[_schemas.StudentShort])
async def get_all_students(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """Получить все зарегистрированные аккаунты студентов """
    logger.debug("")
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_all_students(session)


@fastapi.get("/api/admin/teachers/all", response_model=_typing.List[_schemas.TeacherShort])
async def get_all_teachers(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получить всех зарегистрированные аккаунты учителей """
    logger.debug("")
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_all_teachers(session)


@fastapi.get("/api/teachers/{id}", response_model=_schemas.TeacherFull)
async def get_teacher_account(
    id: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получение странички учителя  """
    logger.debug("")
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_teacher_by_id(id, session)


@fastapi.post("/api/teachers/me", response_model=_schemas.Teacher)
async def teacher_auth(
    data: _schemas.AuthSchema,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Вход в аккаунт учителя по логину и паролю """
    logger.debug("")
    user, teacher = await _services.auth_teacher(data.login, data.password, session)
    return await _cookies.get_signed_response(_services.teacher_model_to_schema(user, teacher), user, session)


@fastapi.get("/api/students/{id}", response_model=_schemas.StudentFull)
async def get_student_by_admin(
    id: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получение странички студента """
    logger.debug("")
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_student_by_id(id, session)


@fastapi.get("/api/verification/{url}", status_code=200)
async def email_verification(
    url: str,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Подтверждение адреса электронной почты пользователя по одноразовой ссылке """
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
    """ png-логотип для статичных HTML-страниц """
    return _fastapi.responses.FileResponse(f"{_os.getcwd()}/data/logos/{name}")


@fastapi.post("/api/applications/company/create", status_code=204)
async def apply_for_company_registration(application: _schemas.CreateCompanyApplicationCreate):
    """ Получение заявок на регистрацию учебных заведений """
    await _applications.add_create_company_application(application)


@fastapi.post("/api/applications/tags/create", status_code=204)
async def apply_for_tags_registration(application: _schemas.CreateTagApplicationCreate):
    """ Получение заявок на добавление тегов профессий """
    await _applications.add_create_tags_application(application)


@fastapi.post("/api/applications/companies/{id}/update", status_code=204)
async def apply_for_company_update(
        id: int,
        application: _schemas.UpdateCompanyApplicationCreate,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получение заявок на изменение данных учебных заведений """
    company = _services.get_company(id, session)
    await _services.check_cookie_and_update_user_online(user, session)
    await _applications.add_update_company_application(application, company)


@fastapi.post("/api/applications/companies/{id}/delete", status_code=204)
async def apply_for_company_deletion(
        id: int,
        application: _schemas.DeleteCompanyApplicationCreate,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получение заявок на удаление учебных заведений """
    company = _services.get_company(id, session)
    await _services.check_cookie_and_update_user_online(user, session)
    await _applications.add_delete_company_application(application, company)


@fastapi.get("/api/applications/all", response_model=_schemas.AllApplications)
async def get_all_applications(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Получение всех необработанных заявок.
    Только для админов
    """
    logger.debug("")
    _, role = await _services.get_account_by_cookie(user, session)
    if role != "admin":
        return _cookies.get_unsign_response()
    return await _applications.get_all_applications()


@fastapi.put("/api/applications/{atype}/{id}", status_code=204)
async def respond_to_application(
    atype: _applications.applications_types,
    id: int,
    decision: _schemas.ApplicationDecision,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):

    """
    Принимает ответы по заявкам. Удаляет заявку и сообщает о решении заявителю по почте


    ВАЖНО:

    Действия, предложенные в заявках, не будут выполнены.
    За данный функционал отвечают другие методы.
    В случае, если было решено принять заявку,
    сначала должен поступить запрос от администратора на выполнение соответствуших действий,
    и только затем вызван данный метод, чтобы оповестить заявителя

    (только для админов)
    """

    _, role = await _services.get_account_by_cookie(user, session)
    if role != "admin":
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
async def get_all_tags(
    session: _orm.Session = _fastapi.Depends(_services.get_db_session),
    user: cookietype = None,
):
    """ Получение всех тегов профессий """
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_all_tags(session)


@fastapi.put("/api/companies/{id}", status_code=204)
async def update_company(
    id: int,
    update: _schemas.CompanyUpdate,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Изменение данных образовательной организации.
    Только для админов
    """
    _, role = await _services.get_account_by_cookie(user, session)
    if role != "admin":
        return _cookies.get_unsign_response()
    await _services.update_company(id, update, session)


@fastapi.delete("/api/companies/{id}", status_code=204)
async def delete_company(
    id: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Удаление образовательной организации.
    Только для админов
    """
    _, role = await _services.get_account_by_cookie(user, session)
    if role != "admin":
        return _cookies.get_unsign_response()
    await _services.drop_company(id, session)


@fastapi.get("/api/companies/all/", response_model=_typing.List[_schemas.Company])
async def get_all_companies(
    page: int = 1,
    pagesize: int = 20,
    desc: bool = False,
    sort: _schemas.companies_sort_types = "name",
    session: _orm.Session = _fastapi.Depends(_services.get_db_session),
    user: cookietype = None,
):
    """ Получить все компании """
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_all_companies(page-1, pagesize, sort, desc, session)


@fastapi.post("/api/courses/", status_code=204)
async def create_course(
        course: _schemas.CourseCreate,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Создание курса.
    Доступно для студентов и учителей, но не для админов
    """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role not in ("student", "teacher"):
        return _cookies.get_unsign_response()
    _services.update_user_online(model, session)
    course = await _services.create_course(course, session)
    _courses.initialize_course(course.id)


@fastapi.get("/api/courses/{id}", response_model=_schemas.Course)
async def get_course(
    id: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получить страничку курса """
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.get_course(id, session)


@fastapi.put("/api/courses/{id}", status_code=204)
async def update_course(
    id: int,
    update: _schemas.CourseUpdate,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Изменить данные на страничке курса.
    Доступно для админов и автора курса
    """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if not role:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if role != "admin" or course.author_id != model.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _services.update_course(course, update, session)


@fastapi.delete("/api/courses/{id}", status_code=204)
async def delete_course(
    id: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Удалить курс.
    Доступно для админов и автора курса
    """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if not role:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if role != "admin" or course.author_id != model.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _services.drop_course(course, session)
    await _courses.drop_course(course.id)


@fastapi.post("/api/courses/{id}/lessons", status_code=204)
async def create_course_lesson(
    id: int,
    data: _schemas.LessonCreate,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Добавление урока к курсу.
    Доступно для админов и автора курса
    """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role not in ("student", "teacher"):
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if course.author_id != model.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    lesson = await _services.create_lesson(course, data, session)
    _courses.initialize_lesson(course.id, lesson.number)


@fastapi.post("/api/courses/{id}/lessons/{number}/steps", response_model=int)
async def create_course_step(
    id: int,
    number: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Добавление шага к уроку.
    Доступно для админов и автора курса
    """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if role not in ("student", "teacher"):
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if course.author_id != model.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _services.get_lesson_model(course, number)
    if not _courses.is_lesson_initialized(id, number):
        raise _fastapi.HTTPException(404, "no such lesson")
    return await _courses.initialize_step(id, number)


@fastapi.post("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/text", status_code=204)
async def set_step_text(
    id: int,
    lesson_number: int,
    step_number: int,
    text: _schemas.StepText,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Загрузка текста для шага урока.
    Доступно для админов и автора курса
    """
    logger.debug("")

    model, role = await _services.get_account_by_cookie(user, session)
    if not role:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    await _services.get_lesson_model(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    if role != "admin" or model.id != course.author.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _courses.write_into_step(id, lesson_number, step_number, text.text)


@fastapi.post("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/image", status_code=204)
async def load_step_image(
    id: int,
    lesson_number: int,
    step_number: int,
    upload: _fastapi.UploadFile,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Загрузка изображения для урока.
    Доступно для админов и автора курса
    """
    logger.debug("")
    model, role = await _services.get_account_by_cookie(user, session)
    if not role:
        return _cookies.get_unsign_response()
    course = _services.get_course_model(id, session)
    if role != "admin" or course.author_id != model.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    await _services.get_lesson_model(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    await _courses.upload_step_image(id, lesson_number, step_number, upload)


@fastapi.get("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/text", response_model=str)
async def get_step_text(
    id: int,
    lesson_number: int,
    step_number: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получить текст урока """
    await _services.check_cookie_and_update_user_online(user, session)
    course = _services.get_course_model(id, session)
    await _services.get_lesson_model(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    return await _courses.get_step_text(id, lesson_number, step_number)


@fastapi.get("/api/courses/{id}/lessons/{lesson_number}/steps/{step_number}/image")
async def get_step_image(
    id: int,
    lesson_number: int,
    step_number: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получить картинку урока """
    await _services.check_cookie_and_update_user_online(user, session)
    course = _services.get_course_model(id, session)
    await _services.get_lesson_model(course, lesson_number)
    if not _courses.is_lesson_initialized(id, lesson_number):
        raise _fastapi.HTTPException(404, "no such lesson")
    return await _courses.get_step_image(id, lesson_number, step_number)


@fastapi.get("/api/courses/{id}/lessons/{number}", response_model=_schemas.LessonFull)
async def get_lesson(
    id: int,
    number: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """ Получить подробную информацию об уроке курса """
    await _services.check_cookie_and_update_user_online(user, session)
    course = _services.get_course_model(id, session)
    return await _services.get_lesson(course, number)


@fastapi.put("/api/courses/{id}/lessons/{number}", status_code=204)
async def update_lesson(
    id: int,
    number: int,
    update: _schemas.LessonUpdate,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Редактирование уроков.
    Доступно для админов и автора курса
    """
    logger.debug("")

    model, role = await _services.get_account_by_cookie(user, session)
    if not role:
        return _cookies.get_unsign_response()

    course = _services.get_course_model(id, session)
    if role != "admin" or course.author_id != model.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    lesson = await _services.get_lesson_model(course, number)
    await _services.update_lesson(lesson, update, session)


@fastapi.delete("/api/courses/{id}/lessons/{number}", status_code=204)
async def delete_lesson(
    id: int,
    number: int,
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    """
    Удаление уроков.
    Доступно для админов и автора курса
    """
    logger.debug("")

    model, role = await _services.get_account_by_cookie(user, session)
    if not role:
        return _cookies.get_unsign_response()

    course = _services.get_course_model(id, session)
    if role != "admin" or course.author_id != model.id:
        raise _fastapi.HTTPException(400, "Permission denied")
    lesson = await _services.get_lesson_model(course, number)
    await _services.drop_lesson(lesson, session)
    await _courses.drop_lesson(lesson.course.id, lesson.number)


@fastapi.get("/api/feed", response_model=_typing.List[_schemas.ShortNews])
async def get_feed(
    user: cookietype = None,
    session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.check_cookie_and_update_user_online(user, session)
    return await _news.get_feed()


@fastapi.get("/api/feed/{id}", response_model=_schemas.FullNews)
async def get_news(
        id: int,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.check_cookie_and_update_user_online(user, session)
    return await _news.get_news_full(id)


@fastapi.get("/api/feed/{nid}/paragraphs/{pid}/image")
async def get_paragraph_image(
        nid: int,
        pid: int,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.check_cookie_and_update_user_online(user, session)
    return await _news.get_paragraph_image(nid, pid)


@fastapi.post("/api/feed", response_model=int)
async def initialize_news(
        data: _schemas.InitNews,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    _, role = await _services.get_account_by_cookie(user, session)
    if not role == "admin":
        return _cookies.get_unsign_response()
    return await _news.init_news(data)


@fastapi.post("/api/feed/{id}", response_model=int)
async def load_paragraph(
        id: int,
        paragraph: _schemas.NewsParagraphCreate,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    _, role = await _services.get_account_by_cookie(user, session)
    if not role == "admin":
        return _cookies.get_unsign_response()
    return await _news.load_paragraph(paragraph, id)


@fastapi.post("/api/feed/{nid}/paragraphs/{pid}/image", status_code=204)
async def load_paragraph_image(
        nid: int,
        pid: int,
        image: _fastapi.UploadFile,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    _, role = await _services.get_account_by_cookie(user, session)
    if not role == "admin":
        return _cookies.get_unsign_response()
    await _news.upload_image(image, nid, pid)


@fastapi.post("/api/courses/search", response_model=_typing.List[_schemas.CourseShort])
async def search_courses(
        tags: _typing.List[int],
        page: int = 1,
        pagesize: int = 20,
        desc: bool = False,
        sort: _schemas.course_search_sorts = "name",
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    await _services.check_cookie_and_update_user_online(user, session)
    return await _services.search_courses(tags, page, pagesize, desc, sort, session)


@fastapi.get("/api/users/me/groups/", response_model=_typing.List[_schemas.Group])
async def get_user_groups(
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    model, role = await _services.get_account_by_cookie(user, session)
    if role == "student":
        return await _services.get_student_groups(model)
    elif role == "teacher":
        return await _services.get_teacher_groups(model)
    else:
        return _cookies.get_unsign_response()


@fastapi.post("/api/groups/", status_code=204)
async def create_group(
        data: _schemas.GroupCreate,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "teacher":
        raise _fastapi.HTTPException(400, "Only teacher can create class")
    await _services.create_group(data.name, model, session)


@fastapi.get("/api/groups/{id}/link", response_model=str)
async def create_join_group_link(
        id: int,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "teacher":
        raise _fastapi.HTTPException(400, "Only teacher can add students to class")
    group = _services.get_group_model(id, session)
    if group.teacher_id != model.user.id:
        return _cookies.get_unsign_response()
    return await _links.create_join_group_link(group, session)


@fastapi.get("/api/groups/join/{url}", status_code=204)
async def join_group_via_link(
        url: str,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    model, role = await _services.get_account_by_cookie(user, session)
    if role != "student":
        raise _fastapi.HTTPException(400, "Only student can join class via link")
    try:
        await _links.join_group(url, model, session)
    except _links.LinkJoinUseless:
        resp = await _staticpages.get_link_join_useless_page()
        resp.status_code = 400
        return resp
    except _links.LinkInvalidError:
        resp = await _staticpages.get_link_invalid_page()
        resp.status_code = 400
        return resp


@fastapi.delete("/api/groups/{gid}/students/{sid}", status_code=204)
async def ban_student_from_group(
        gid: int,
        sid: int,
        user: cookietype = None,
        session: _orm.Session = _fastapi.Depends(_services.get_db_session)
):
    _, role = await _services.get_account_by_cookie(user, session)
    if role != "teacher":
        return _cookies.get_unsign_response()
    student = _services.get_student_model(sid, session)
    group = _services.get_group_model(gid, session)
    await _services.ban_from_group(student, group, session)
