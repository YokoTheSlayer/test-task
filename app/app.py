"""Модуль основного приложения.

Собирает, подключает и инициализирует все необходимые зависимости,
подприложения, и маршрутизирует запросы.
"""

import os
import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp_oauth2 import oauth2_app

from .auth import auth_context_processor, setup_auth
from app import handlers
from .users import setup_users
from .mongo import setup_mongo
from .sessions import setup_sessions
from .routes import ROUTES
from .http import setup_http


async def create_app() -> aiohttp.web.Application:
    """Создаём основное приложение.

    Returns:
        aiohttp.web.Application: Приложение
    """
    app = aiohttp.web.Application()
    setup_sessions(app)
    app.add_routes(ROUTES)
    setup_mongo(app,
                host=os.getenv('MONGO_HOST'),
                db_name=os.getenv('MONGO_DB'),
                username=os.getenv('MONGO_USER'),
                password=os.getenv('MONGO_PWD'))
    setup_users(app)
    setup_auth(app)
    setup_http(app)
    app.router.add_static('/static', path='static', name='static')
    app['static_root_url'] = '/static'
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(['app/templates',
                                                         ]),
                         context_processors=[auth_context_processor,
                                             ],
                         extensions=['jinja2.ext.do'])
    app.add_subapp(
        "/google/",
        oauth2_app(
            client_id=os.getenv('GOOGLE_ID'),
            client_secret=os.getenv('GOOGLE_SECRET'),
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            token_url="https://www.googleapis.com/oauth2/v4/token",
            scopes=['email'],
            on_login=handlers.google_callback,
        ))

    return app
