During my work on this project I practiced with the technologies:

- asyncio;
- aiohttp;
- PostgreSQL;
- SQLAlchemy;
- websockets.

This is a small site with a radio stream translated from an icecast server with mpd.
There is a possibility to vote for the next track after login.

What to do to make it work:

**Install and configure postgres (Ubuntu):**

sudo apt install postgresql  
sudo -i -u postgres  
psql  
CREATE USER radio_admin WITH PASSWORD 'radio_admin';  
CREATE DATABASE radio_logins;

To exit from psql and postgres user:

\q  
exit

After that create all the tables in the database with this:
python init_db.py

**Install and configure icecast and mpd:**

sudo apt install icecast2  
sudo apt install mpc mpd

Mpd doesn't create folders and files for its correct working,
so you need to do this:

mkdir ~/.config  
mkdir ~/.config/mpd  
touch ~/.mpd/{mpd.db,mpd.log,mpd.pid,mpdstate}

Configs for mpd and Icecast you can take from 'Icecast and mpd configs' folder.
Put the config for Icecast in '/etc/icecast2/icecast.xml' and the config for mpd 'in ~./config/mpd/mpd.conf'.

Start icecast with 'sudo systemctl enable icecast2.service'. Start mpd with 'mpd ~./config/mpd/mpd.conf'
After that populate mpd database with the command 'mpc update',
then add music to the playlist with 'mpc ls | mpc add'. Then start the server with 'python main.py'.
