import os as _os
import typing as _typing
import json as _json
import datetime as _dt

import aiofiles as _aiofiles
import pydantic as _pydantic
from loguru import logger as _logger

import schemas as _schemas
import tg as _tg
from emails import emails as _emails


"""
Работа с заявками на изменение чувствительных данных

"""


applications_types = _typing.Literal[
    "create_company",
    "delete_company",
    "update_company",
    "create_tags"
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


async def add_create_company_application(
        application: _schemas.CreateCompanyApplicationCreate
):
    try:
        async with _aiofiles.open(
                _os.path.normpath(f"{_os.getcwd()}/applications/companies/create.json"),
                "r",
                encoding="utf-8"
        ) as file:
            schema = _schemas.CreateCompanyApplication(**application.dict(), id=1, date=_dt.datetime.utcnow())
            try:
                existing = _pydantic.parse_raw_as(_typing.List[_schemas.CreateCompanyApplication], await file.read())
            except _json.JSONDecodeError:
                existing = []
            if existing:
                schema.id = max(a.id for a in existing) + 1
            existing.append(schema)
        async with _aiofiles.open(
                _os.path.normpath(f"{_os.getcwd()}/applications/companies/create.json"),
                "w",
                encoding="utf-8"
        ) as file:
            await file.write(_json.dumps(list(serialize_schema(sc) for sc in existing), indent=4))
            await _tg.application("Добавление учебной организации", str(application.dict()))
            await _emails.send_create_company_promise_email(application.applicant_email)
    except Exception as e:
        _logger.error(f"failed to save applications {e}")
        await _tg.error(f"Не удалось обработать заявку\n\n\aЗаявка:\n{application.dict()}\n\n{e=}")


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
            _schemas.DeleteCompanyApplication
        )
        return _schemas.AllApplications(
            tags=create_tags,
            companies=companies
        )
    except Exception as e:
        _logger.error(f"unable to read applications: {e}")
        await _tg.error(f"Не удалось прочитать заявки\n\n{e=}")


async def get_application(appl: applications_types, id: int):
    path, schema = application_type_data(appl)
    applications = await _get_applications(path, schema)
    for a in applications:
        if a.id == id:
            return a


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
