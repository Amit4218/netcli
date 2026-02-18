import json
import math
import shutil
import os
import platform
import subprocess
from datetime import datetime
from pathlib import Path

from .contants import HISTORY_FILE


HISTORY_FILE = Path(HISTORY_FILE)


def clear_screen():
    """cleans the terminal"""
    if platform.system() == "windows":
        os.system("cls")
    else:
        os.system("clear")


def search_helper(response) -> bool:
    """helper for : SoapScraper -> search checks for application/json response.header content-Type"""
    return "application/json" in response.headers.get("content-type", "").lower()


def get_stream(resp) -> bool:
    """helper for : SoapScraper -> checks the file type for .m3u8 and relevent content-type"""
    url = resp.url.lower()
    ctype = resp.headers.get("content-type", "").lower()

    return ".m3u8" in url and (
        "mpegurl" in ctype
        or "playlist" in url
        or "master" in url
        or "application/vnd.apple.mpegurl" in url
        or "audio/x-mpegurl" in url
    )


def start_player(url, referrer="https://ployan.live"):
    """helper to strat streaming the movie or series"""
    subprocess.run(["mpv", f"--referrer={referrer}", url])
    

def print_adaptive_grid(items, padding=4, min_col_width=18):
    term_width = shutil.get_terminal_size().columns

    longest = max(len(i) for i in items) if items else 0
    col_width = max(min_col_width, longest + 2)

    cols = max(1, term_width // (col_width + padding))
    rows = math.ceil(len(items) / cols)

    for r in range(rows):
        line = ""
        for c in range(cols):
            idx = r + c * rows
            if idx < len(items):
                line += items[idx].ljust(col_width) + " " * padding
        print(line.rstrip())


def save_history(data):
    """maintains history of watched movies / series metadata"""

    data["watched_at"] = datetime.now().strftime("%d-%m-%Y")

    # load history
    if HISTORY_FILE.exists(): # type: ignore
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []
    else:
        history = []

    # check if already exists
    for item in history:
        if item["title"].lower() == data["title"].lower():
            if item["type"] != data["type"]:
                break

            if data["type"] == "movie":
                item["metadata"] = data["metadata"]
                item["watched_at"] = data["watched_at"]
                break

            elif data["type"] == "series":
                item["metadata"].update(data["metadata"])
                item["watched_at"] = data["watched_at"]
                break

    else:
        history.append(data)

    # save back
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)
