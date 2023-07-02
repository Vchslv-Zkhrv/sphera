import os as _os
import datetime as _dt
import typing as _typing

import aiofiles as _aiofiles
from sqlalchemy import orm as _orm

import schemas as _schemas
import models as _models


class Chat():

    """ Объект-обертка для работы с чатами """

    path: str
    model = _models.Chat

    def __init__(self, model: _models.Chat):
        path = f"{_os.getcwd()}/chats/chats/{model.id}.chat"
        if not _os.path.isfile(path):
            raise FileNotFoundError
        self.path = path

    async def append(
            self,
            message: _schemas.MessageCreate,
            se: _orm.Session
    ):
        se.refresh(self.model)
        if message.sender not in (m.user_id for m in self.model.members):
            raise ValueError("sender not in chat")
        ids = await self.get_ids()
        id = max(ids) + 1 if ids else 1
        full = _schemas.Message(
            s=message.sender,
            t=message.text,
            m=message.media,
            d=_dt.datetime.utcnow(),
            i=id
        )
        async with _aiofiles.open(self.path, "a", encoding="utf-8") as file:
            await file.write(full.json(by_alias=True) + "\n")

    async def get_ids(self) -> _typing.List[int]:
        ids = []
        async for m in self.messages():
            ids.append(m.id)
        return ids

    async def get(self, id: int):
        async with _aiofiles.open(self.path, "r+", encoding="utf-8") as file:
            while True:
                line = await file.readline()
                if not line:
                    raise IndexError("No such message")
                message = _schemas.Message.parse_raw(line)
                if message.id == id:
                    return message

    async def messages(self):
        async with _aiofiles.open(self.path, "r", encoding="utf-8") as file:
            async for line in file:
                yield _schemas.Message.parse_raw(line)

    async def rowcount(self):
        return len(await self.get_ids())

    def destroy(self, se: _orm.Session):
        se.refresh(self.model)
        for member in self.model.members:
            se.delete(member)
            se.commit()
        se.delete(self.model)
        se.commit()
        _os.remove(self.path)

    @staticmethod
    def create(chat: _models.Chat):
        path = f"{_os.getcwd()}/chats/chats/{chat.id}.chat"
        open(path, "x", encoding="utf-8")
        return Chat(chat)
