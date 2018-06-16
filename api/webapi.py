from aiohttp import web, WSCloseCode
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
            return {"error": "No such method"}

        if data['method'] in self._items:
            return await self._items[data['method']](request, data)



routes = web.RouteTableDef()
methods = APIMethods()

async def on_shutdown(app: web.Application):
    for ws in set(app['websockets']):
        await ws.close(code=WSCloseCode.GOING_AWAY, message="Hub shutting down...")

@routes.get("/sosaki_socket")
async def ws_handler(request: web.Request):
    session = await get_session(request)
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['websockets'].add(ws)

    async for msg in ws:
        data = await msg.receive_json()
        ws.send_json(await methods.call(data))



@methods.add("login")
async def authorize(request: web.Request, data: dict):
    session = await get_session(request)
    if session['verified']:
        return {"message": "Already logged, opening panel..."}

    if 'login' not in data or not 'password' in data:
        return {"error": "Not enough parameters"}

    password = request.app['db'].execute("SELECT password FROM users WHERE username = (?)", (data['login'], ))

    if len(password):
        if password[0] == sha512(data['password']):
            session['verified'] = True
            return {"message": f"Welcome, {data['login']}"}
        else:
            session['verified'] = False

    return {"message": f"Wrong login or password"}