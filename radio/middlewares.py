from typing import Callable, Awaitable

import aiohttp_session
from aiohttp import web

_WebHandler = Callable[[web.Request], Awaitable[web.StreamResponse]]


def require_login(func: _WebHandler) -> _WebHandler:
    func.__require_login__ = True  # type: ignore
    return func


@web.middleware
async def check_login(request, handler: _WebHandler):
    req_login = getattr(handler, "__require_login__", False)
    session = await aiohttp_session.get_session(request)
    username = session.get("login")
    if req_login:
        if not username:
            raise web.HTTPSeeOther(location="/login")
    return await handler(request)
