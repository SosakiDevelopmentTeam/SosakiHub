import asyncio
import base64

from cryptography import fernet

from api import *
from hub_repos import *

if not is_win:
    import uvloop


def run_app(loop):
    app = web.Application()

    app['db'] = DB("database.db")
    app['sockets'] = []
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