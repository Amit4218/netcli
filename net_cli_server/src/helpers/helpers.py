import secrets
import subprocess
import requests


def start_player(url, referrer="https://ployan.live"):
    """helper to strat streaming the movie or series"""
    subprocess.Popen(
        ["mpv", "--really-quiet", "--no-terminal", f"--referrer={referrer}", url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def get_movie_urls(movie_id: str):
    """helper to get the playable movie urls"""
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://vidnest.fun/",
        "Origin": "https://vidnest.fun",
        "Content-Type": "application/json",
    }

    # get the timestamps
    trace = session.get("https://vido-player.pages.dev/cdn-cgi/trace")
    trace_data = dict(line.split("=", 1) for line in trace.text.strip().split("\n"))
    timestamp = int(float(trace_data["ts"]))

    # Get the encrypted data for the movie
    movie = session.get(
        f"https://new.vidnest.fun/allmovies/movie/{movie_id}"  # example id -> 1061474
    )
    enc_data = movie.json()["data"]

    # Structure the payload
    payload = {
        "data": enc_data,
        "timestamp": timestamp,
        "nonce": secrets.token_hex(16),  # generate a once usable token
    }

    # Get the decrypted data
    response = session.post(
        "https://new.vidnest.fun/decrypt", headers=headers, json=payload
    )

    data = response.json()["data"]["streams"]
    return data
