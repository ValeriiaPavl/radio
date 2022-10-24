import asyncio
import sys
from typing import Optional

import aiohttp_jinja2
import aiohttp_session
import jinja2
from aiohttp import web

from db import pg_context
from player.player_simulator import RadioPlayer
from routes import setup_routes
from settings import config, BASE_DIR
from middlewares import check_login

app = web.Application()
app['db_config'] = config
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / 'radio' / 'templates')))
setup_routes(app)
app.cleanup_ctx.append(pg_context)
aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())

fake_player: Optional[RadioPlayer] = None
app.middlewares.append(check_login)
folder = (sys.argv[1:])[0]


async def main(folder):
    global fake_player
    fake_player = RadioPlayer(folder)
    fake_player.start()
    app['fake_player'] = fake_player
    await asyncio.gather(web._run_app(app),
                         fake_player.wait_for_background_job())


asyncio.run(main(folder))
