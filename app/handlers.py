import os

import aiohttp
from aiohttp import web
from aiohttp_jinja2 import template
from .auth.utils import authorize_user, encrypt_password
from app.auth.handlers import UserStatus
from app.users.user_repository import UserRepository
from .mongo import Mongo


@template('index.html')
async def index(request):
    return {}


@template('success_page.html')
async def success(request):
    return {}


@template('login.html')
async def login(request):
    return {}


@template('success.html')
async def google_callback(request, google_callback):
    users = UserRepository(Mongo(host=os.getenv('MONGO_HOST'),
                                 db_name=os.getenv('MONGO_DB'),
                                 username=os.getenv('MONGO_USER'),
                                 password=os.getenv('MONGO_PWD')).db)

    params = {}
    if 'access_token' in google_callback:
        params['access_token'] = google_callback['access_token']
        params['alt'] = 'json'
        headers = {
            "Authorization": f"Bearer {google_callback['access_token']}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://www.googleapis.com/oauth2/v1/userinfo', params=params) as r:
                response = await r.json()
    user = await users.find_user({'email': response['email']})
    if not user:
        user = await users.create_user({
            'lastName': None,
            'firstName': None,
            'email': response['email'],
            'password': encrypt_password(response['id']),
            'status': UserStatus.ACTIVE.value,
        })
        await authorize_user(request, user, db=users)
    else:
        await authorize_user(request, user, db=users)
    return web.HTTPTemporaryRedirect(location="/success")
