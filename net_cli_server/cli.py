import typer
from rich.console import Console
from rich.prompt import Prompt
from src.scraper.search_movie import search_query
from src.scraper.get_movies import scrape_movie_link
from src.scraper.get_episode import scrape_episode_link
from src.helpers.cli_helper import ask_for_user_choice
from src.helpers.helpers import start_player

# rich console for pretty printing
console = Console()

app = typer.Typer(help="search and watch movies through you'r terminal")


@app.command()
def main():
    try:
        movie_name = Prompt.ask("[bold cyan]Enter the name of the movie: ")

        # search for the movie
        with console.status(f"[bold yellow]Searching for {movie_name}..."):
            results = search_query(query=movie_name)

        if not results:
            raise Exception("No movies found!")

        # ask the user to chose a movie/series
        selected = ask_for_user_choice(
            items=[m["title"] for m in results],
            message="Please Select the movie/series",
        )

        # filter the selected movie/series
        selected_movie = results[selected]

        with console.status(
            f"[bold yellow] Searching for {selected_movie['title']}..."
        ):
            movie_result = scrape_movie_link(movie_link=selected_movie["link"])

        if not movie_result["movie"]:
            episodes = movie_result["episodes"]
            selected = ask_for_user_choice(
                items=[ep for ep in movie_result["episodes"]],
                message="Please select the episode",
            )
            selected_episode = episodes[selected]

            with console.status(
                f"[bold yellow] Searching for {selected_episode} of {selected_movie['title']}"
            ):
                link_found = scrape_episode_link(
                    ep_id=selected_episode, movie_link=movie_result["base_link"]
                )

                if link_found:
                    console.print("[bold green] Episode found, Playing now...")
                    start_player(url=link_found)

        else:
            languages = movie_result["language"]
            selected_language = ask_for_user_choice(
                items=[lang["language"] for lang in languages],
                message="Please select a language",
            )

            movie = languages[selected_language]
            console.print("[bold green] Playing now...")
            start_player(url=movie["url"], referrer=movie["headers"]["Referer"])

    except Exception as e:
        console.print(e)


if __name__ == "__main__":
    app()
