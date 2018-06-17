import aiosqlite


class DB:

    def __init__(self, db_name):
        self.name = db_name

    async def execute(self, command, params=(), commit=True):
        async with aiosqlite.connect(self.name) as db:
            cur = await db.execute(command, params)
            data = [el for el in await cur.fetchall()]
            if commit:
                await db.commit()
            await cur.close()
            await db.close()
            return data
