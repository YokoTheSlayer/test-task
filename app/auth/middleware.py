from aiohttp import web

from .settings import SETTINGS
from .utils import get_current_user


@web.middleware
async def current_user_middleware(request: web.Application, handler) -> web.Response:
    """Добавляем пользователя в request, если он есть"""
    request[SETTINGS['REQUEST_USER_KEY']] = await get_current_user(request)
    return await handler(request)
