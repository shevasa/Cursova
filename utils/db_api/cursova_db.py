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

    async def get_genres(self):
        sql = "SELECT name FROM genres WHERE True"
        return await self.execute(sql, fetch=True)

    async def task2(self, genre):
        sql = """select a.name as artist_name, g.name as genre
                    from artist_genre ag
                        left join artists a on ag.artist_id = a.id
                        left join genres g on ag.genre_id = g.id
                    where g.name=$1"""
        return await self.execute(sql, genre, fetch=True)

    async def get_impressarios_names(self):
        sql = "SELECT name FROM impressarios WHERE TRUE"
        return await self.execute(sql, fetch=True)

    async def task3(self, impressario_name):
        sql = """select a.name as artist_name, i.name as impressario_name
                    from artist_impressario ai
                             left join artists a on ai.artist_id = a.id
                             left join impressarios i on ai.impressarios_id = i.id
                    where i.name = $1"""
        return await self.execute(sql, impressario_name, fetch=True)

    async def task4(self):
        sql = """select a.name as artist_name, g.name as genre
                    from (select artist_id, count(genre_id) from artist_genre ag group by artist_id having count(genre_id) > 1) ac
                        left join artists a on ac.artist_id = a.id
                        left join artist_genre ag on ag.artist_id = a.id
                        left join genres g on g.id = ag.genre_id
                    ORDER BY a.name;"""
        return await self.execute(sql, fetch=True)

    async def get_artists_names(self):
        sql = "SELECT name FROM artists where True"
        return await self.execute(sql, fetch=True)

    async def task5(self, artist_name):
        sql = """select a.name as artist_name, i.name as impressario_name
                    from artist_impressario ai
                        left join artists a on ai.artist_id = a.id
                        left join impressarios i on ai.impressarios_id = i.id
                    where a.name = $1"""
        return await self.execute(sql, artist_name, fetch=True)

    async def task6(self, min_event_date, max_event_date):
        sql = """select se.name as event_name, se.date, et.name as type_of_event, sp.name as place, o.name as organizator
                    from specific_event se
                        left join organizers o on se.organizer_id = o.id
                        left join specific_place sp on se.place_id = sp.id
                        left join event_types et on se.type_id = et.id
                        where date > $1 and date < $2"""
        return await self.execute(sql, min_event_date, max_event_date, fetch=True)

    async def task7(self, concurs):
        sql = """select concurs.name as concurs_name, a.name as participant_name, cp.place as place
                    from (select id, name from specific_event where type_id = 3) concurs
                             left join concurs_participants cp on concurs.id = cp.id_concurs
                             left join artists a on cp.id_participant = a.id
                    where cp.place < 4
                      AND cp.place > 0
                      AND concurs.name = $1
                    order by cp.place asc"""
        return await self.execute(sql, concurs, fetch=True)

    async def get_concurs_name(self):
        sql = "SELECT name FROM specific_event where type_id=3"
        return await self.execute(sql, fetch=True)

    async def get_place_name(self):
        sql = "SELECT name FROM specific_place WHERE TRUE"
        return await self.execute(sql, fetch=True)

    async def task8(self, place):
        sql = """select se.name as event_name, place.name as place
                    from (select id, name from specific_place where name = $1) place
                             inner join specific_event se on place.id = se.place_id;"""
        return await self.execute(sql, place, fetch=True)
