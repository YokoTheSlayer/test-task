"""Модуль для работы с HTTP-клиентом."""
import aiohttp
from aiohttp import ClientSession


def setup_http(app: aiohttp.web.Application):
    """Подключить http-клиент к приложению.

    Args:
        app (aiohttp.web.Application): Приложение, к которому производится подключение.
    """
    app['http'] = ClientSession()

    async def _close(app: aiohttp.web.Application):
        await app['http'].close()

    app.on_cleanup.append(_close)
