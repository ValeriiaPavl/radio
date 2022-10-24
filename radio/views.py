import aiohttp_jinja2
from middlewares import require_login


@aiohttp_jinja2.template('player page.html')
async def player_page(request):
    return


@aiohttp_jinja2.template('login_page.html')
async def logging(request):
    return


@aiohttp_jinja2.template('signup.html')
async def signup_page(request):
    return


@require_login
@aiohttp_jinja2.template('song_voting.html')
async def voting(request):
    return
