import json
import threading

from bottle import request, route, run
from src.scraper.get_episode import scrape_episode_link
from src.scraper.get_movies import scrape_movie_link
from src.scraper.search_movie import search_query
from src.utils.constants import MOVIE_PLAYER
from src.utils.scheduler import movie_scheduler


@route("/<movie>", method="GET")
def search(movie):
    result = search_query(str(movie))
    return json.dumps(result)


@route("/verify", method="POST")
def verify():
    data = request.json
    link = data.get("url")  # type: ignore
    result = scrape_movie_link(link)
    return json.dumps(result)


@route("/get", method="POST")
def episode():
    data = request.json
    result = scrape_episode_link(ep_id=data.get("ep_id"), movie_link=(data.get("link")))  # type: ignore
    MOVIE_PLAYER.put(result)
    return {"success": True, "message": "playing the now"}

@route("/play", method="POST")
def play():
    data = request.json
    movie = {"link":data["link"], "referrer":data["referrer"] if data["referrer"] else None}
    MOVIE_PLAYER.put(movie)
    return {"success":True}

if __name__ == "__main__":
    threading.Thread(target=movie_scheduler, daemon=True).start()
    run(host="0.0.0.0", port=6789)




