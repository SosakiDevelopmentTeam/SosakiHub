import asyncio
import base64

from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from cryptography import fernet

from api import *
from hub_repos import *
import weakref

if not is_win:
    import uvloop


def run_app(loop):
    app = web.Application(loop=loop)
    # Sessions storage key generation
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key, cookie_name="sosaki_session", max_age=300))

    app['db'] = DB("database.db")
    app['websockets'] = weakref.WeakSet()
    app.router.add_routes(routes)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host='localhost', port=8080)
    return app


if __name__ == "__main__":
    if is_win:
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    run_app(loop)