from aiohttp import web
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select
import aiohttp_session
from player.player_simulator import RadioPlayer
import db


async def do_sign_up(request):
    request_data = await request.post()
    ph = PasswordHasher()
    with (await request.app['db']) as conn:
        await conn.execute(
            db.site_login.insert(),
            {'login': request_data['login'],
             'password_hash_sum': ph.hash(request_data['password'])})
    raise web.HTTPSeeOther(location="/login")


async def do_login(request):
    request_data = await request.post()
    ph = PasswordHasher()
    with (await request.app['db']) as conn:
        async with conn.execute(select(db.site_login).where(
                db.site_login.c.login == request_data['login'])) as cursor:
            for row in await cursor.fetchall():
                try:
                    ph.verify(row.password_hash_sum, request_data['password'])
                    session = await aiohttp_session.get_session(request)
                    session["login"] = request_data["login"]
                    raise web.HTTPSeeOther(location="/song_voting")
                except VerifyMismatchError:
                    print('The login or password were wrong')
                    raise web.HTTPForbidden


async def logout(request):
    session = await aiohttp_session.get_session(request)
    session["login"] = None
    raise web.HTTPSeeOther(location="/")


async def add_user_vote(request):
    user_choice = await request.post()
    fake_player: RadioPlayer = request.app['fake_player']
    session = await aiohttp_session.get_session(request)
    user = session["login"]
    fake_player.voters_choice_list[user] = user_choice['song_for_vote']
    print(fake_player.voters_choice_list)

    raise web.HTTPSeeOther(location="/")
