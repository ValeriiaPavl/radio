import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, String)


from sqlalchemy.dialects.postgresql import TEXT

meta = MetaData()

site_login = Table('site_login', meta,
                   Column('login', String(50), primary_key=True),
                   Column('password_hash_sum', TEXT, nullable=False))


async def pg_context(app):
    conf = app['db_config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
