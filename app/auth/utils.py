"""Вспомогательные утилиты для пакета авторизации."""
import random
import string
from datetime import datetime, timedelta

import passlib.hash
from aiohttp_session import get_session

from .settings import SETTINGS

CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits


def get_random_string(min_: int, max_: int = None) -> str:
    """Произвольная строка

    Args:
        min_ (int): Минимальная длина строки.
        max_ (int, optional): Максимальная длина строки. Defaults to None.

    Returns:
        str: Произвольно сгенерированная строка.
    """
    max_ = max_ or min_
    size = random.randint(min_, max_)
    return ''.join(random.choice(CHARS) for x in range(size))


def encrypt_password(password):
    return passlib.hash.sha256_crypt.encrypt(password, rounds=1000)


def check_password(password, password_hash):
    return passlib.hash.sha256_crypt.verify(password, password_hash)


def is_confirmation_expired(confirmation):
    age = datetime.utcnow() - confirmation['createdAt']
    lifetime_days = SETTINGS['{}_CONFIRMATION_LIFETIME'.format(
        confirmation['action'].upper())]
    lifetime = timedelta(days=lifetime_days)
    return age > lifetime


async def authorize_user(request, user, db=None):
    session = await get_session(request)
    if 'users' not in request.app:
        session[SETTINGS['SESSION_USER_KEY']] = db.user_session_id(user)
        return
    users = request.app['users']
    session[SETTINGS['SESSION_USER_KEY']] = users.user_session_id(user)


async def get_current_user_id(request):
    session = await get_session(request)

    user_id = session.get(SETTINGS['SESSION_USER_KEY'])
    while user_id:
        if not isinstance(user_id, str) or not user_id:
            break

        return user_id

    if SETTINGS['SESSION_USER_KEY'] in session:
        del session['user']


async def get_current_user(request, db=None):
    users = request.app['users']
    user_id = await get_current_user_id(request)
    if user_id:
        user = await users.find_user({'id': user_id})
        if not user:
            session = await get_session(request)
            del session['user']
        return user
