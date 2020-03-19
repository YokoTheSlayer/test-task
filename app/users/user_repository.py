"""Репозиторий пользователей"""
from datetime import datetime
from enum import Enum
from logging import getLogger
from uuid import uuid4

from bson import ObjectId

# pylint: disable=invalid-name
logger = getLogger('UserRepository')


class UserStatus(str, Enum):
    """Статус пользователя."""

    ACTIVE = 'active'
    CONFIRMATION = 'confirmation'
    ANONYMOUS = 'anonymous'


class UserRepository:
    _collection = 'users'

    def __init__(self, db):
        self.users = db[self._collection]

    def user_session_id(self, user):
        return str(user['id'])

    async def find_user(self, filter_):
        if 'id' in filter_:
            filter_['_id'] = ObjectId(filter_.pop('id'))

        user = await self.users.find_one(filter_)
        if not user:
            return None

        user['id'] = str(user.pop('_id'))

        return user

    async def create_user(self, data):
        data.setdefault('createdAt', datetime.utcnow())
        data.setdefault('status', UserStatus.ANONYMOUS)
        data.setdefault('guid', uuid4())

        result = await self.users.insert_one(data)

        return await self.find_user({'id': result.inserted_id})

    async def update_user(self, user, updates):
        return await self.users.update_one({
            '_id': user['id']
        }, {
            '$set': {
                **updates,
                'updatedAt': datetime.utcnow(),
            }
        })

    async def delete_user(self, user):
        return await self.users.delete_one({
            '_id': user['id']
        })
