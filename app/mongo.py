"""Модуль для работы с Mongo."""
from aiohttp import web
from motor.motor_tornado import MotorClient


def setup_mongo(app: web.Application, *,
                db_name: str = 'testtask',
                host: str = None,
                username: str = None,
                password: str = None):
    """Подключение MongoDB к приложению

    Args:
        app (aiohttp.web.Application): Приложение, к которому производится подключение.
        db_name (str, optional): Название базы данных. По умолчанию 'cms'.
        host (str, optional): Хост. По умолчанию None.
        username (str, optional): Пользователь. По умолчанию None.
        password (str, optional): Пароль. По умолчанию None.
    """
    app['mongo'] = Mongo(db_name, host, username, password)
    app['db'] = app['mongo'].db
    app.on_startup.append(app['mongo'].init)
    app.on_cleanup.append(app['mongo'].close)


class Mongo(object):
    def __init__(self, db_name, host=None, username=None, password=None):
        self._db_name = db_name
        params = {
            'host': host,
            'username': username,
            'password': password,
        }
        params = {k: v for k, v in params.items() if v}
        if 'username' in params or 'password' in params:
            params['authSource'] = db_name
            params['authMechanism'] = 'SCRAM-SHA-1'

        self._mongo = MotorClient(f"mongodb+srv://{username}:{password}@{host}/{db_name}?retryWrites=true&w=majority")
        self._db = self._mongo[self._db_name]

    async def get_next_sequence_value(self, sequence_name: str) -> dict:
        result = await self._db.command(
            'findAndModify',
            findAndModify='counters',
            query={"_id": sequence_name},
            update={"$inc": {"sequenceValue": int(1)}},
            upsert=True)

        value = result['value']

        if not value:
            return 0
        return value['sequenceValue']

    async def init(self, *args, **kwargs):
        pass

    async def close(self, *args, **kwargs):
        self._mongo.close()

    @property
    def db(self):
        return self._db
