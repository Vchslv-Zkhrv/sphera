import os as _os
import typing as _typing
import json as _json

import aiofiles as _aiofiles
import pydantic as _pydantic
from loguru import logger as _logger

import schemas as _schemas
import tg as _tg
from emails import emails as _emails


"""
Работа с заявками на изменение чувствительных данных

"""


async def add_create_company_application(
        application: _schemas.CreateCompanyApplication
):
    try:
        async with _aiofiles.open(
                _os.path.normpath(f"{_os.getcwd()}/applications/companies/create.json"),
                "r",
                encoding="utf-8"
        ) as file:
            try:
                existing = _pydantic.parse_raw_as(_typing.List[_schemas.CreateCompanyApplication], await file.read())
            except _json.JSONDecodeError:
                existing = []
            existing.append(application)
        async with _aiofiles.open(
                _os.path.normpath(f"{_os.getcwd()}/applications/companies/create.json"),
                "w",
                encoding="utf-8"
        ) as file:
            await file.write(_json.dumps(list(schema.dict() for schema in existing)))
            await _tg.application("Добавление учебной организации", str(application.dict()))
            await _emails.send_create_company_promise_email(application.applicant_email)
    except Exception as e:
        _logger.error(f"failed to save applications {e}")
        await _tg.error(f"Не удалось обработать заявку\n\n\aЗаявка:\n{application.dict()}\n\n{e=}")
        raise e
