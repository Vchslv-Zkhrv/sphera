import os as _os
import datetime as _dt
import typing as _typing

import aiofiles as _aiofiles
import fastapi as _fastapi

import schemas as _schemas


def _get_news_ids():
    return list(map(int, _os.listdir(f"{_os.getcwd()}/news/news")))


async def init_news(data: _schemas.InitNews):
    ids = _get_news_ids()
    new_id = max(ids) + 1 if ids else 1
    schema = _schemas.FullNews(
        id=new_id,
        date=_dt.date.today(),
        title=data.title,
        paragraphs=[]
    )
    async with _aiofiles.open(f"{_os.getcwd()}/news/news/{new_id}.json", "w", encoding="utf-8") as file:
        await file.write(schema.json(indent=4))
    return new_id


async def load_paragraph(paragraph: _schemas.NewsParagraphCreate, news_id: int):
    if not _os.path.isfile(f"{_os.getcwd()}/news/news/{news_id}.json"):
        raise _fastapi.HTTPException(404, "no such news") 
    async with _aiofiles.open(f"{_os.getcwd()}/news/news/{news_id}.json", "r", encoding="utf-8") as file:
        schema = _schemas.FullNews.parse_raw(await file.read())
    pid = max(p.id for p in schema.paragraphs)+1 if schema.paragraphs else 1
    if paragraph.kind == "image src":
        paragraph.content = f"/api/feed/{news_id}/paragraphs/{pid}/image"
    fullp = _schemas.NewsParagraph.parse_obj({"id": pid, **paragraph.dict()})
    schema.paragraphs.append(fullp)
    async with _aiofiles.open(f"{_os.getcwd()}/news/news/{news_id}.json", "w", encoding="utf-8") as file:
        await file.write(schema.json(indent=2))
    return pid


async def get_feed() -> _typing.List[_schemas.ShortNews]:
    feed = []
    for name in _os.listdir(f"{_os.getcwd()}/news/news"):
        async with _aiofiles.open(f"{_os.getcwd()}/news/news/{name}", "r", encoding="utf-8") as file:
            feed.append(_schemas.ShortNews.parse_raw(await file.read()))
    return feed


async def get_news_full(id: int):
    if not _os.path.isfile(f"{_os.getcwd()}/news/news/{id}.json"):
        raise _fastapi.HTTPException(404, "no such news")
    async with _aiofiles.open(f"{_os.getcwd()}/news/news/{id}.json", "r", encoding="utf-8") as file:
        return _schemas.FullNews.parse_raw(await file.read())


async def upload_image(upload: _fastapi.UploadFile, nid: int, pid: int):
    ext = upload.filename.split(".")[-1].lower()
    if ext not in ("png", "jpg", "jpeg"):
        raise _fastapi.HTTPException(415, "Unsupportable image type")
    if upload.size > 1048576:
        raise _fastapi.HTTPException(413, "Image too large")
    async with _aiofiles.open(
        f"{_os.getcwd()}/news/images/{nid}-{pid}.{ext}",
        "wb"
    ) as file:
        content = await upload.read()
        await file.write(content)


async def get_paragraph_image(nid: int, pid: int):
    images = tuple(filter(
        (lambda name: f"{nid}-{pid}" in name),
        _os.listdir(f"{_os.getcwd()}/news/images")
    ))
    if not images:
        raise _fastapi.HTTPException(404, "No such image")
    image_name = images[0]
    return _fastapi.responses.FileResponse(f"{_os.getcwd()}/news/images/{image_name}")


def drop_news(news_id):
    if not _os.path.isfile(f"{_os.getcwd()}/news/news/{news_id}.json"):
        raise _fastapi.HTTPException(404, "no such news") 
    _os.remove(f"{_os.getcwd()}/news/news/{news_id}.json")


async def get_paragraph(nid: int, pid: int):
    if not _os.path.isfile(f"{_os.getcwd()}/news/news/{nid}.json"):
        raise _fastapi.HTTPException(404, "no such news")
    async with _aiofiles.open(f"{_os.getcwd()}/news/news/{nid}.json", "r", encoding="utf-8") as file:
        schema = _schemas.FullNews.parse_raw(await file.read())
    for p in schema.paragraphs:
        if p.id == pid:
            return (schema, p)
    raise _fastapi.HTTPException(404, "no such paragraph")


async def drop_paragraph(nid: int, pid: int):
    schema, paragraph = await get_paragraph(nid, pid)
    schema.paragraphs.remove(paragraph)
    async with _aiofiles.open(f"{_os.getcwd()}/news/news/{nid}.json", "w", encoding="utf-8") as file:
        await file.write(schema.json(indent=2))
