from player.player_simulator import RadioPlayer
from aiohttp import web
import json


async def render_track_name(request):
    fake_player: RadioPlayer = request.app['fake_player']
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    while True:
        await ws.send_str(str(fake_player.current_track.name))
        await fake_player.wait_for_next_track()


async def render_vote_options(request):
    fake_player: RadioPlayer = request.app['fake_player']
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    while True:
        tracks_for_vote = fake_player.songs_for_vote
        await ws.send_str(json.dumps([track.name for track in tracks_for_vote]))
        await fake_player.wait_for_next_track()
