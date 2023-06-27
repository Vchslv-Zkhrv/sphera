import datetime as _datetime
import hashlib as _hashlib

from sqlalchemy import orm as _orm

import models as _models
import schemas as _schemas
from config import DOMAIN as _DOMAIN

"""
Работа с ссылками на выполнение действий

"""


class LinkError(Exception):
    pass


class LinkInvalidError(LinkError):
    pass


class LinkOverusedError(LinkError):
    pass


class LinkExpiredError(LinkError):
    pass


class LinkJoinUseless(LinkError):
    pass


class AccountNotActivatedError(LinkError):
    pass


async def create_verify_email_link(
        user: _models.User,
        se: _orm.Session
):
    url = _hashlib.sha1(str(_datetime.datetime.now().timestamp()).encode()).hexdigest()
    link = _models.Link(
        url=url,
        limit=1,
        target=user.id,
        action="verify email",
        date_expired=_datetime.datetime.now() + _datetime.timedelta(hours=1)
    )
    se.add(link)
    se.commit()
    return link


def get_link_by_url(
        url: str,
        se: _orm.Session
):
    link = se.query(_models.Link).filter_by(url=url).first()
    if not link:
        raise LinkInvalidError
    schema = _schemas.Link.from_orm(link)
    if link.limit:
        if link.limit <= link.count_used:
            se.delete(link)
            se.commit()
            raise LinkOverusedError
    if schema.date_expired:
        if schema.date_expired < _datetime.datetime.now():
            se.delete(link)
            se.commit()
            raise LinkExpiredError
    return link


async def verify_email(
        url: str,
        se: _orm.Session
):
    link = get_link_by_url(url, se)
    user = se.get(_models.User, link.target)
    if not user:
        raise LinkInvalidError
    user.confirmed = True
    link.count_used += 1
    se.commit()
    se.refresh(user)


async def create_join_group_link(
        group: _models.Group,
        se: _orm.Session
):
    old = se.query(_models.Link).filter_by(target=group.id).filter_by(action="join group").first()
    if old:
        return f"{_DOMAIN}/api/groups/join/{old.url}"
    url = _hashlib.sha1(str(_datetime.datetime.now().timestamp()).encode()).hexdigest()
    link = _models.Link(
        url=url,
        target=group.id,
        action="join group",
    )
    se.add(link)
    se.commit()
    return f"{_DOMAIN}/api/groups/join/{url}"


async def join_group(
        url: str,
        student: _models.User,
        se: _orm.Session
):
    link = get_link_by_url(url, se)
    group = se.get(_models.Group, link.target)
    if not group:
        raise LinkInvalidError
    if student.id in (s.student_id for s in group.students):
        raise LinkJoinUseless
    gs = _models.GroupStudents(
        student_id=student.id,
        group_id=group.id
    )
    se.add(gs)
    se.commit()
    se.refresh(gs)
    link.count_used += 1
    se.commit()
    se.refresh(group)
