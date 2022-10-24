from forms import do_login, do_sign_up, add_user_vote, logout
from views import player_page, logging, voting, signup_page
from render_data_from_player import render_vote_options, render_track_name


def setup_routes(app):
    app.router.add_get('/', player_page)
    app.router.add_get('/login', logging)
    app.router.add_post('/login', do_login)
    app.router.add_post('/signup', do_sign_up)
    app.router.add_get('/signup', signup_page)
    app.router.add_get('/track', render_track_name)
    app.router.add_get('/song_voting', voting)
    app.router.add_get('/options', render_vote_options)
    app.router.add_post('/song_voting', add_user_vote)
    app.router.add_get('/logout', logout)
