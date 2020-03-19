"""Пакет для работы с пользователями."""
import aiohttp

from .user_repository import UserRepository
from .user_repository import UserStatus


def setup_users(app: aiohttp.web.Application):
    """Подключение сервиса для работы с пользователями

    Args:
        app (aiohttp.web.Application): Приложение, к которому подключается сервис.
    """
    app['users'] = UserRepository(app['db'])
