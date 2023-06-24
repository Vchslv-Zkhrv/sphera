import os as _os
import typing as _typing
import json as _json
import datetime as _dt

import aiofiles as _aiofiles
import pydantic as _pydantic
from loguru import logger as _logger
import fastapi as _fastapi
from sqlalchemy import orm as _orm

import schemas as _schemas
import tg as _tg
from emails import emails as _emails
import models as _models
import services as _services


"""
Работа с заявками на изменение чувствительных данных

"""


applications_types = _typing.Literal[
    "create_company",
    "delete_company",
    "update_company",
    "create_tags"
]

application_create_types = _typing.Union[
    _schemas.CreateCompanyApplicationCreate,
    _schemas.CreateTagApplicationCreate,
    _schemas.UpdateCompanyApplicationCreate,
    _schemas.DeleteCompanyApplicationCreate
]

application_json_types = _typing.Union[
    _schemas.CreateCompanyApplication,
    _schemas.CreateTagApplication,
    _schemas.UpdateCompanyApplication,
    _schemas.DeleteCompanyApplication
]


def application_type_data(atype: applications_types) -> _typing.Tuple[str, _schemas._JsonApplicationBase]:
    return {
        "create_company": (f"{_os.getcwd()}/applications/companies/create.json", _schemas.CreateCompanyApplication),
        "update_company": (f"{_os.getcwd()}/applications/companies/update.json", _schemas.UpdateCompanyApplication),
        "delete_company": (f"{_os.getcwd()}/applications/companies/delete.json", _schemas.DeleteCompanyApplication),
        "create_tags": (f"{_os.getcwd()}/applications/tags/create.json", _schemas.CreateTagApplication),
    }[atype]


def serialize_schema(schema: _pydantic.BaseModel):
    dct = schema.dict()
    for key, value in dct.items():
        if isinstance(value, (_dt.datetime, _dt.time, _dt.datetime)):
            dct[key] = value.isoformat()
    return dct


async def _create_application(
        application: application_create_types,
        to_type: _typing.Type[application_json_types],
        path: str,
        purpose: str,
        email_method: _typing.Coroutine,
        **email_kwargs
):
    try:
        async with _aiofiles.open(path, "r", encoding="utf-8") as file:
            schema = to_type(**application.dict(), id=1, date=_dt.datetime.utcnow())
            try:
                existing = _pydantic.parse_raw_as(_typing.List[to_type], await file.read())
            except _json.JSONDecodeError:
                existing = []
            if existing:
                schema.id = max(a.id for a in existing) + 1
            existing.append(schema)
        async with _aiofiles.open(path, "w", encoding="utf-8") as file:
            await file.write(_json.dumps(list(serialize_schema(sc) for sc in existing), indent=4))
            await _tg.application(purpose, str(application.dict()))
            await email_method(application.applicant_email, **email_kwargs)
    except Exception as e:
        _logger.error(f"failed to save applications {e}")
        await _tg.error(f"Не удалось обработать заявку\n\n\aЗаявка:\n{application.dict()}\n\n{e=}")


async def add_create_company_application(application: _schemas.CreateCompanyApplicationCreate):
    await _create_application(
        application=application,
        to_type=_schemas.CreateCompanyApplication,
        path=_os.path.normpath(f"{_os.getcwd()}/applications/companies/create.json"),
        purpose="Добавление учебной организации",
        email_method=_emails.send_create_company_promise_email
    )


async def add_create_tags_application(application: _schemas.CreateTagApplicationCreate):
    await _create_application(
        application=application,
        to_type=_schemas.CreateTagApplication,
        path=_os.path.normpath(f"{_os.getcwd()}/applications/tags/create.json"),
        purpose="Добавление тегов профессий",
        email_method=_emails.send_create_tags_promise_email
    )


async def add_update_company_application(
        application: _schemas.UpdateCompanyApplicationCreate,
        company: _models.Company
):
    await _create_application(
        application=application,
        to_type=_schemas.UpdateCompanyApplication,
        path=_os.path.normpath(f"{_os.getcwd()}/applications/companies/update.json"),
        purpose="Изменение данных учебной организации",
        email_method=_emails.send_update_company_promise_email,
        company=company
    )


async def add_delete_company_application(
            appliaction: _schemas.DeleteCompanyApplicationCreate,
            company: _models.Company
):
    await _create_application(
        application=appliaction,
        to_type=_schemas.DeleteCompanyApplication,
        path=_os.path.normpath(f"{_os.getcwd()}/applications/companies/delete.json"),
        purpose="Удаление учебной организации",
        email_method=_emails.send_delete_company_promise_email,
        company=company
    )


async def _get_applications(file: str, schema: _typing.Type[_schemas._JsonApplicationBase]):
    async with _aiofiles.open(_os.path.normpath(file), "r", encoding="utf-8") as file:
        try:
            return _pydantic.parse_raw_as(_typing.List[schema], await file.read())
        except _json.JSONDecodeError:
            return []


async def get_all_applications():
    try:
        create_companies = await _get_applications(
            f"{_os.getcwd()}/applications/companies/create.json",
            _schemas.CreateCompanyApplication
        )
        update_companies = await _get_applications(
            f"{_os.getcwd()}/applications/companies/update.json",
            _schemas.UpdateCompanyApplication
        )
        delete_companies = await _get_applications(
            f"{_os.getcwd()}/applications/companies/delete.json",
            _schemas.DeleteCompanyApplication
        )
        companies = _schemas.AllCompanyApplications(
            create=create_companies,
            update=update_companies,
            delete=delete_companies
        )
        create_tags = await _get_applications(
            f"{_os.getcwd()}/applications/tags/create.json",
            _schemas.CreateTagApplication
        )
        return _schemas.AllApplications(
            tags=create_tags,
            companies=companies
        )
    except Exception as e:
        _logger.error(f"unable to read applications: {e}")
        await _tg.error(f"Не удалось прочитать заявки\n\n{e=}")
        raise _fastapi.HTTPException(409, "Cannot to read applications")


async def get_application(appl: applications_types, id: int):
    try:
        path, schema = application_type_data(appl)
        applications = await _get_applications(path, schema)
        for a in applications:
            if a.id == id:
                return a
    except Exception as e:
        _logger.error(f"cannot find any applications {e=}")
        return None


async def delete_application(appl: applications_types, id: int):
    try:
        path, schema = application_type_data(appl)
        applications = await _get_applications(path, schema)
        copy = applications[:]
        for i, ap in enumerate(applications):
            if ap.id == id:
                copy.pop(i)
        async with _aiofiles.open(path, "w", encoding="utf-8") as file:
            await file.write(_json.dumps(list(serialize_schema(sc) for sc in copy), indent=4))
    except Exception as e:
        _logger.error(f"unable to delete application: {appl=} {id=}")
        await _tg.error(f"Не удалось удалить заявку {appl=} {id=}:\n\n{e=}")
