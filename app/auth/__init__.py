"""Пакет для работы с авторизацией."""
import aiohttp

from .context_processors import auth_context_processor
from .middleware import current_user_middleware
from .utils import get_current_user


def setup_auth(app: aiohttp.web.Application):
    """Подключение сервиса

    Args:
        app (aiohttp.web.Application): Приложение, к которому подключается сервис.
    """
    async def _setup(app: aiohttp.web.Application):
        app.middlewares.append(current_user_middleware)

    app.on_startup.append(_setup)
