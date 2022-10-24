import random
from typing import NamedTuple
import os.path
import mutagen


class Track(NamedTuple):
    name: str
    duration: float
    path: str


def get_track_data(path: str) -> Track:
    audio = mutagen.File(path)
    track_name = f'{audio["artist"][0]} - {audio["title"][0]}'
    track_duration = audio.info.length
    rel_path = os.path.basename(path)
    return Track(name=track_name, duration=track_duration, path=rel_path)


def get_random_track(folder) -> str:
    track_list = os.listdir(folder)
    random_track = random.choice(track_list)
    path_to_track = os.path.join(folder, random_track)
    return get_track_data(path_to_track)
