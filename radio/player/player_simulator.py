import asyncio
import os
import sys
from player.track import get_random_track
from player.mpc_stuff import MpdPlayer
from collections import defaultdict


class RadioPlayer:
    def __init__(self, folder: str, player=MpdPlayer(), options_number=2):
        self.folder = folder
        self.track_list = os.listdir(folder)
        self.current_track = get_random_track(self.folder)
        self.next_track_event = asyncio.Event()
        self._background_job = None
        self.player = player

        self.options_number = options_number
        self.songs_for_vote = self.choose_vote_songs()
        self.voters_choice_list = {}

    async def _background_job_implementation(self):
        self.player.clear_playlist()
        self.player.add_track(track=self.current_track.path)
        while True:
            await asyncio.sleep(self.current_track.duration - 1)
            self.current_track = self.get_best_song()
            self.reset_vote_data()
            self.next_track_event.set()
            self.next_track_event.clear()
            self.player.add_track(track=self.current_track.path)

    def start(self):
        self._background_job = asyncio.create_task(self._background_job_implementation())

    async def wait_for_background_job(self):
        await self._background_job

    async def wait_for_next_track(self):
        await self.next_track_event.wait()

# methods for voting
    def choose_vote_songs(self):
        tracks_for_voting = [get_random_track(self.folder) for i in range(self.options_number)]
        return tracks_for_voting

    def reset_vote_data(self):
        self.songs_for_vote = self.choose_vote_songs()
        # print(self.songs_for_vote)
        self.voters_choice_list.clear()

    def get_best_song(self):
        votes_result = defaultdict(lambda: 0)
        for song in self.voters_choice_list.values():
            votes_result[song] += 1
        max_vote = 0
        best_song = None
        for song, vote_result in votes_result.items():
            if vote_result >= max_vote:
                best_song = song
        if best_song is None:
            return self.songs_for_vote[0]
        best_song_number = int(best_song.split(' ')[1])
        return self.songs_for_vote[best_song_number]


music_folder = (sys.argv[1:])[0]


async def main():
    player = RadioPlayer(music_folder, options_number=2)
    player.start()
    await player.wait_for_background_job()


if __name__ == '__main__':
    asyncio.run(main())
