from aiohttp import web, WSCloseCode, WSMsgType
import json, logging
from hashlib import sha512 as _sha512
from collections.abc import Sequence
import time, random

sha512 = lambda x: _sha512(x.encode('utf-8')).hexdigest()
sessionExistsTime = 300

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

    async def call(self, sock, data):
        if 'method' not in data:
            return {"type": "error", "content": "No such method"}

        if data['method'] in self._items:
            return await self._items[data['method']](sock, data)


routes = web.RouteTableDef()

cb_id = lambda d: d.get('cb_id', 0)


async def on_shutdown(app):
    for ws in set(app['sockets']):
        await ws.close(code=WSCloseCode.GOING_AWAY, message="Hub shutting down...")

methods = APIMethods()

@routes.get("/socket")
class Socket(web.View):

    async def get(self):
        ws = web.WebSocketResponse(autoclose=False)
        await ws.prepare(self.request)

        self.request.app['sockets'].append(ws)

        async for msg in ws:
            self.deleteOldSessions()
            if msg.type == WSMsgType.TEXT:
                data = None

                try:
                    data = json.loads(msg.data)
                except Exception as e:
                    logging.error(f'Error while loading JSON: {e.__str__()}')
                    break

                if data.get('session'): self.updateSession(data['session'])
                await ws.send_json(await methods.call(self, data))

            elif msg.type == WSMsgType.CLOSE:
                break;
            else:
                continue

        self.request.app['sockets'].remove(ws)

        return ws


    @methods.add('check_auth')
    async def check_auth(self, data: dict):

        if not data.get('session'):
            return {"type": "error", "content": "User not authorized.", "cb_id": cb_id(data)}

        session = await self.checkSession(data['session'])
        id = await self.getIdBySession(data['session'])

        if session:
            return {"type": "user_id", "content": "Already logged", "user_id": id, "session": data['session'], "cb_id": cb_id(data)}

        await self.deleteSession(session)
        return {"type": "session_expired"}


    @methods.add('login')
    async def authorize(self, data: dict):
        d = await self.check_auth(data)

        if d['type'] != "error": return d

        if 'login' not in data or 'password' not in data:
            return {"type": "error", "content": "Not enough parameters", "cb_id": cb_id(data)}

        user_id = await self.check_password(data)

        if user_id:
            session = await self.createSession(user_id)
            return {"type": "user_id", "content": f"Welcome, {data['login']}", "session": session, "user_id": user_id, "cb_id": cb_id(data)}

        return {"type": "error", "content": "Wrong login or password", "cb_id": cb_id(data)}

    async def check_password(self, data):
        creds = await self.request.app['db'].execute('SELECT password, id FROM users WHERE username = (?)',
                                                       (data['login'],))
        if len(creds):
            if creds[0][0] == sha512(data['password']):
                return creds[0][1]
        return False

    async def checkSession(self, sess):
        session = await self.request.app['db'].execute('SELECT session FROM sessions WHERE session=(?) AND (?) < removal_time', (sess, time.time()))
        if len(session) != 0:
            return True
        return False

    async def deleteOldSessions(self):
        await self.request.app['db'].execute('delete from sessions where (?) > removal_time', (time.time(),), True)

    async def deleteSession(self, session):
        await self.request.app['db'].execute('delete from sessions where session=(?) ', (session,), True)

    async def updateSession(self, session):
        await self.deleteOldSessions()
        await self.request.app['db'].execute("update sessions set removal_time=(?) where session=(?)", (time.time() + sessionExistsTime, session),
                 True)

    def generateSession(self):
        return sha512(str(random.randint(0, 2 ** 256)) + str(random.randint(0, 2 ** 256)))

    async def getIdBySession(self, session):
        data = await self.request.app['db'].execute("select user_id from sessions where session=(?)", (session,))

        if len(data) == 0:
            return 0

        return data[0][0]

    async def createSession(self, user_id):
        session = self.generateSession()
        createTime = time.time()

        await self.request.app['db'].execute("insert or replace into sessions (session, user_id, removal_time) values (?, ?, ?)",
                 (session, user_id, createTime + sessionExistsTime), True)
        return session

# TODO: Add new methods
