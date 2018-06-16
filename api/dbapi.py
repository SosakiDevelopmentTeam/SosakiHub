import aiosqlite


class DB:

    def __init__(self, db_name):
        self.database: aiosqlite.Connection = aiosqlite.connect(db_name)

    async def execute(self, command, params=(), commit=True):
        async with self.database as db:
            cur = await db.execute(command, params)
            data = [el for el in await cur.fetchall()]
            if commit:
                self.database.commit()
            await cur.close()

            return data

    async def close(self):
        await self.database.close()
