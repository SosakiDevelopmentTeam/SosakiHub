from hub_repos import *
from aiohttp import web
import asyncio

async def handle(request):
    ...

async def main():
    ...

if __name__ == "__main__":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    tasks = [loop.create_task(main())]
    loop.run_until_complete(asyncio.wait(tasks))