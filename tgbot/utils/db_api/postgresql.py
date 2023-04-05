import asyncio
import asyncpg
import tgbot.config 




class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
            user = config.DbConfig.user,
            password = config.DbConfig.password,
            host = config.DbConfig.host
            )
        )

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXIST Users (
        id INT NOT NULL,
        Name VARCHAR(255),
        Status VARCHAR(255),
        PRIMARY KEY (id);
        )
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id INT NOT NULL,
        name VARCHAR(355) NOT NULL,
        status VARCHAR(255),
        PRIMARY KEY (id);
        )
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ])

    async def add_user(self, id: int, name: str, status: str):
        sql = "INSERT INTO Users (id, name, status) VALUES ($1, $2, $3)"
        await self.pool.execute(sql, id, name, status)


    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.pool.fetch(sql)
    
    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)
    
    async def count_users(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Users")

    async def update_status(self, status, id):
        sql = "UPDATE Users SET status = $1 WHERE id = $2"
        return await self.pool.execute(sql, status, id)
           
    async def remove_user(self, id):
        await self.pool.execute("DELETE FROM Users WHERE id = $1")

    async def select_status(self, id):
        sql = "SELECT status FROM Users WHERE id = $1"
        return await self.pool.execute(sql, id)
