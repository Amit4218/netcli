import questionary
from typing import List


def ask_for_user_choice(items: List[str], message: str) -> None:
    choices = [questionary.Choice(title=item, value=i) for i, item in enumerate(items)]
    choice = questionary.select(message, choices=choices).ask()
    return choice
