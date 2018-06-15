from hub_repos import *
from aiohttp import web
import asyncio

async def handle(request):
    ...

async def main():
    ...

if __name__ == "__main__":
    if is_win:
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    tasks = [loop.create_task(main())]
    loop.run_until_complete(asyncio.wait(tasks))