from argon2 import PasswordHasher
from sqlalchemy import create_engine, MetaData

from radio.db import site_login
from radio.settings import config

params = config['postgres']
db_name = params['database']
db_user = params['user']
db_pass = params['password']

db_host = params['host']
db_port = params['port']


def setup_db(conf):
    admin_user_url = "postgresql://postgres:postgres@localhost:5432"
    admin_engine = create_engine(admin_user_url, isolation_level='AUTOCOMMIT')
    conn = admin_engine.connect()
    conn.execute(f"DROP DATABASE IF EXISTS {db_name}")
    conn.execute(f"DROP ROLE IF EXISTS {db_user}")
    conn.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_pass}'")
    conn.execute(f"CREATE DATABASE {db_name} ENCODING 'UTF8'")
    conn.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")
    conn.close()


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[site_login])


def sample_data(engine):
    ph = PasswordHasher()
    conn = engine.connect()
    conn.execute(site_login.insert(), [
        {'login': 'lera',
         'password_hash_sum': ph.hash('1234')}
    ])
    conn.close()


if __name__ == '__main__':
    setup_db(config)
    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    user_engine = create_engine(db_url)
    create_tables(user_engine)
    sample_data(user_engine)
