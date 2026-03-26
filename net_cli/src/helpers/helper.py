import subprocess
import questionary
from typing import List
from src.utils.constants import CONSOLE, THEME


def ask_for_user_choice(items: List[str], message: str) -> int:
    """helper to print movies/series for selection"""
    choices = [questionary.Choice(title=item, value=i) for i, item in enumerate(items)]
    choice = questionary.select(message, choices=choices).ask()
    return choice


def stream_movie(url, referrer="https://ployan.live") -> None:

    mpv_cmd = [
        "mpv",
        "--really-quiet",
        "--no-terminal",
        f"--referrer={referrer}",
        url,
    ]

    CONSOLE.print(f"{THEME['success']} Playing now...")
    subprocess.Popen(mpv_cmd)
