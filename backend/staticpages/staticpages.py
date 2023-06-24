import os as _os

import fastapi as _fastapi
import aiofiles as _aiofiles

from config import DOMAIN as _DOMAIN
import schemas as _schemas


"""
Выдача html - страниц в ответ на прямые запросы к серверу

"""


async def get_static_page(
        template_name: _schemas.static_templates,
        src: _schemas.static_logos
):
    async with _aiofiles.open(
            f"{_os.getcwd()}/staticpages/templates/{template_name}.html", "r", encoding="utf-8"
    ) as html:
        content = await html.read()
        content = content.replace("!SRC!", f"{_DOMAIN}/api/images/static/{src}")
        return _fastapi.responses.HTMLResponse(content=content)


async def get_verify_email_success_page():
    return await get_static_page("verify_email_success", "logo.png")


async def get_link_expired_page():
    return await get_static_page("link_expired", "alter-logo.png")


async def get_link_overused_page():
    return await get_static_page("link_overused", "alter-logo.png")


async def get_link_join_useless_page():
    return await get_static_page("link_join_useless", "alter-logo.png")


async def get_link_invalid_page():
    return await get_static_page("link_invalid", "alter-logo.png")


async def get_account_not_activated_page():
    return await get_static_page("account_not_activated", "alter-logo.png")


async def get_link_500_error_page():
    return await get_static_page("internal_server_error", "alter-logo.png")
