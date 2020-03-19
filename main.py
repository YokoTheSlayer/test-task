import os

import aiohttp
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    from app.app import create_app

    aiohttp.web.run_app(create_app(),
                        host=os.getenv('HOST', '0.0.0.0'),
                        port=os.getenv('PORT', '8080'))
