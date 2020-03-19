from aiohttp import web
from . import handlers
from .auth import handlers as h_auth

AUTH_PREFIX = '/auth'
ROUTES = [
    web.get('/', handlers.index, name="index"),
    web.get('/auth/logout', h_auth.logout, name='auth:logout'),
    web.post('/auth/register', h_auth.register, name='auth:register'),
    web.post('/auth/login', h_auth.login, name='auth:login'),
    web.get('/success', handlers.success, name="success"),
    web.get('/login_page', handlers.login, name='login'),
]
