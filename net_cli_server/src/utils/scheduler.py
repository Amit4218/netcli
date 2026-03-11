import time

from src.helpers.helpers import start_player

from .constants import MOVIE_PLAYER


def movie_scheduler():
    while True:
        if not MOVIE_PLAYER.empty():
            movie = MOVIE_PLAYER.get()
            
            if movie["link"] and movie["referrer"]:
                start_player(movie["link"], movie["referrer"])
            else:
                start_player(url=movie["link"]) 

        time.sleep(2)
