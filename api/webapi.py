from aiohttp import web, WSCloseCode, WSMsgType
from aiohttp_session import get_session
import json, logging
from hashlib import sha512 as _sha512
from collections.abc import Sequence

sha512 = lambda x: _sha512(x.encode('utf-8')).hexdigest()


class APIMethods(Sequence):
    """API methods table"""

    def __init__(self):
        self._items = {}

    def __repr__(self):
        return "<APIMethods count={}>".format(len(self._items))

    def __getitem__(self, name):
        return self._items[name]

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def add(self, name):
        def inner(handler):
            self._items[name] = handler
            return handler

        return inner

    async def call(self, request, data):
        if 'method' not in data:
            return {"type": "error", "content": "No such method"}

        if data['method'] in self._items:
            return await self._items[data['method']](request, data)


routes = web.RouteTableDef()
methods = APIMethods()

cb_id = lambda d: d.get('cb_id', 0)

async def on_shutdown(app: web.Application):
    for ws in set(app['sockets']):
        await ws.close(code=WSCloseCode.GOING_AWAY, message="Hub shutting down...")


async def check_password(request, data):
    creds = await request.app['db'].execute('SELECT password, id FROM users WHERE username = (?)', (data['login'],))
    if len(creds):
        if creds[0][0] == sha512(data['password']):
            return creds[0][1]
    return False

@routes.get("/")
async def ws_handler(request: web.Request):
    session = await get_session(request)  # Maybe because of session??
    ws = web.WebSocketResponse(autoclose=False)

    await ws.prepare(request)

    if ws not in request.app['sockets']:
        request.app['sockets'].append(ws)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            data = None

            try:
                data = json.loads(msg.data)
            except Exception as e:
                logging.error(f'Error while loading JSON: {e.__str__()}')
                break
            await ws.send_json(await methods.call(request, data))

        elif msg.type == WSMsgType.CLOSE:
            break
        else:
            continue

    await ws.close()
    request.app['sockets'].remove(ws)

    return ws


@methods.add("login")
async def authorize(request: web.Request, data: dict):
    session = await get_session(request)
    if 'verified' in session and session['verified']:
        return {"type": "message", "content": "Already logged, opening panel...", "cb_id": cb_id(data)}

    if 'login' not in data or 'password' not in data:
        return {"type": "error", "content": "Not enough parameters", "cb_id": cb_id(data)}

    user_id = check_password(request, data)
    if user_id:
        session['verified'] = True
        return {"type": "user_id", "content": f"Welcome, {data['login']}", "user_id": user_id, "cb_id": cb_id(data)}

    session['verified'] = False
    return {"type": "error", "content": "Wrong login or password", "cb_id": cb_id(data)}

# TODO: Add new methods
