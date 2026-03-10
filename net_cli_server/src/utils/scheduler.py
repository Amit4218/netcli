import time

from src.helpers.helpers import start_player

from .constants import MOVIE_PLAYER


def movie_scheduler():
    while True:
        if not MOVIE_PLAYER.empty():
            movie = MOVIE_PLAYER.get()
            print("playing")
            start_player(movie["link"], movie["referrer"])

        time.sleep(2)
