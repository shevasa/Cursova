import logging
from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from data import config


class Database:
    def __init__(self):
        self.pool: Union[None, Pool] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      fetch: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    async def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def task1(self, **kwargs):
        logging.info(f"{kwargs=}")
        if "min_max_number_of_seats" not in kwargs.keys():
            if kwargs:
                sql = """select sp.name, sp.number_of_seats, sp.address 
                from specific_place sp
                 inner join infrastructure_types it
                            on sp.type_id = it.id
                where """
                sql, parameters = await self.format_args(sql, kwargs)
                return await self.execute(sql, *parameters, fetch=True)
            else:
                sql = """select sp.name, sp.number_of_seats, sp.address 
                from specific_place sp
                 inner join infrastructure_types it
                            on sp.type_id = it.id"""
                return await self.execute(sql, fetch=True)
        elif "min_max_number_of_seats" in kwargs.keys():
            min_max_number = kwargs.get("min_max_number_of_seats")
            min_number = list(min_max_number.split("-"))[0]
            max_number = list(min_max_number.split("-"))[1]
            kwargs.__delitem__('min_max_number_of_seats')
            sql = f"""select sp.name, sp.number_of_seats, sp.address 
                        from specific_place sp
                         inner join infrastructure_types it
                                    on sp.type_id = it.id
                        where sp.number_of_seats>{min_number} AND sp.number_of_seats<{max_number}"""
            if kwargs:
                sql += " AND "
                sql, parameters = await self.format_args(sql, kwargs)
                return await self.execute(sql, *parameters, fetch=True)
            else:
                return await self.execute(sql, fetch=True)