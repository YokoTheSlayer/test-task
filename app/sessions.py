"""Модуль для работы с сессиями пользователей."""
import base64

import aiohttp
from aiohttp_session import SimpleCookieStorage, session_middleware
from aiohttp_session import setup as setup_session
from aiohttp_session_mongo import MongoStorage
from cryptography.fernet import Fernet

SESSION_COLLECTION_KEY = 'sessions'


def setup_sessions(app: aiohttp.web.Application):
    """Подключение сессионного хранилища к приложению

    Args:
        app (aiohttp.web.Application): Приложение, к которому производится подключение.
    """
    async def _setup(app: aiohttp.web.Application):
        session_collection = app['db'][SESSION_COLLECTION_KEY]
        max_age = 3600 * 24 * 365  # 1 year
        setup_session(app, MongoStorage(session_collection, max_age=max_age))
    fernet_key = Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    _cookie_storage = SimpleCookieStorage()
    app.middlewares.append(session_middleware(_cookie_storage))
    app.on_startup.append(_setup)
