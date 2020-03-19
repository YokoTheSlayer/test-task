import aiohttp
from aiohttp_session import get_session

from .utils import get_current_user


async def auth_context_processor(request: aiohttp.web.Request) -> dict:
    return {
        'user': await get_current_user(request),
    }
