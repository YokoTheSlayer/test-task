from enum import Enum
from http import HTTPStatus

import marshmallow as mm
import pyfacebook
from aiohttp import web
from aiohttp_session import get_session

from .settings import MESSAGES, SETTINGS
from .utils import (
    authorize_user,
    check_password,
    encrypt_password
)


class UserStatus(str, Enum):
    """Статус пользователя."""

    ACTIVE = 'active'
    CONFIRMATION = 'confirmation'
    ANONYMOUS = 'anonymous'


def bad_request(errors):
    return web.json_response({
        'errors': errors
    }, status=HTTPStatus.BAD_REQUEST)


class RegisterRequestSchema(mm.Schema):
    lastName = mm.fields.String(required=True)
    firstName = mm.fields.String(required=True)
    email = mm.fields.Email(required=True)
    password = mm.fields.String(required=True)


async def register(request: web.Request):
    """Регистрация нового пользователя."""
    try:
        data = RegisterRequestSchema().load(await request.post())
    except mm.exceptions.ValidationError as err:
        return bad_request(err.messages)

    users = request.app['users']

    # Создаём нового пользователя
    user = await users.create_user({
        'lastName': data['lastName'],
        'firstName': data['firstName'],
        'email': data['email'],
        'password': encrypt_password(data['password']),
        'status': UserStatus.ACTIVE.value,
    })

    # Авторизуем пользователя
    await authorize_user(request, user)

    # Возвращаем редирект на необходимую страницу
    link = request.app.router['success'].url_for()
    raise web.HTTPFound(location=link)


class LoginRequestSchema(mm.Schema):
    email = mm.fields.Email(required=True)
    password = mm.fields.String(required=True)


async def login(request: web.Request):
    """Аутентификация пользователя."""
    try:
        data = LoginRequestSchema().load(await request.post())
    except mm.exceptions.ValidationError as err:
        return bad_request(err.messages)
    errors = []

    users = request.app['users']

    user = await users.find_user({'email': data['email']})
    if not user:
        errors.append(MESSAGES['UNKNOWN_EMAIL'])
    elif not check_password(data['password'], user['password']):
        errors.append(MESSAGES['WRONG_PASSWORD'])

    if errors:
        return web.json_response({
            'errors': errors
        }, status=HTTPStatus.BAD_REQUEST)

    # Авторизуем пользователя
    await authorize_user(request, user)

    # Возвращаем редирект на необходимую страницу
    location = request.app.router['success'].url_for()
    raise web.HTTPFound(location=location)


async def logout(request: web.Request):
    """Завершение сессии пользователя."""
    session = await get_session(request)
    session.pop(SETTINGS['SESSION_USER_KEY'], None)
    link = str(request.app.router['index'].url_for())
    raise web.HTTPFound(location=link)


async def facebook_auth(request: web.Request):
    """Обработка ответа от FB
    Требуется подтверждение приложения для полноценной работы
    """
    FB_ID = '518326962426522'
    FB_SECRET = '1c665c7fc2a9eb0d42c12e89da5babf2'
    api = pyfacebook.Api(
        app_id=FB_ID,
        app_secret=FB_SECRET,
        application_only_auth=True)

