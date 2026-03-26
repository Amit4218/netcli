import typer
from src.scrapers import get_movies
from src.utils.constants import CONSOLE, THEME
from src.scrapers.search_movie import search_query
from src.scrapers.get_movies import scrape_movie_link
from src.scrapers.get_episode import scrape_episode_link
from src.scrapers.get_suggestion import get_movie_recomendations
from src.helpers.helper import ask_for_user_choice, stream_movie
from rich.panel import Panel
from rich.prompt import Prompt

app = typer.Typer(help="search and watch movies through your terminal")


@app.command(help="search movie and series")
def search(
    movie: str | None = typer.Option(
        None, "--movie", "-s", help="Name of the movie/series"
    )
):

    try:

        movie_name = movie
        if not movie_name:
            movie_name = Prompt.ask(f"{THEME['search']}Enter the name of the movie: ")

        # search for the movie
        with CONSOLE.status(f"{THEME['searching']}Searching for {movie_name}..."):
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

        with CONSOLE.status(
            f"{THEME['searching']}Searching for {selected_movie['title']}..."
        ):
            movie_result = scrape_movie_link(movie_link=selected_movie["link"])

        # if the selected_movie is a series
        if not movie_result["movie"]:
            episodes = movie_result["episodes"]
            selected = ask_for_user_choice(
                items=[ep for ep in movie_result["episodes"]],
                message="Please select the episode",
            )

            selected_episode = episodes[selected]

            with CONSOLE.status(
                f"{THEME['searching']} Searching for {selected_episode} of {selected_movie['title']}"
            ):
                link_found = scrape_episode_link(
                    ep_id=selected_episode, movie_link=movie_result["base_link"]
                )

            # play the selected episode
            stream_movie(url=link_found)

        else:
            stream_movie(url=movie_result["link"])

    except Exception as e:
        CONSOLE.print(f"{THEME['error']} {e}")


@app.command(help="get movies/series suggestions")
def suggest():
    try:
        results = get_movie_recomendations()
        CONSOLE.print(
            f"{THEME['searching']}Here are some movies/series we think you might me intrested in"
        )

        choice = ask_for_user_choice(
            items=[sm["name"] for sm in results], message="Select the one you like"
        )

        with CONSOLE.status(
            f"{THEME['searching']}Searching for {results[choice]['name']}..."
        ):
            movie_result = scrape_movie_link(movie_link=results[choice]["link"])

        # if the selected_movie is a series
        if not movie_result["movie"]:
            episodes = movie_result["episodes"]
            selected = ask_for_user_choice(
                items=[ep for ep in movie_result["episodes"]],
                message="Please select the episode",
            )

            selected_episode = episodes[selected]

            with CONSOLE.status(
                f"{THEME['searching']} Searching for {selected_episode} of  {results[choice]['name']}"
            ):
                link_found = scrape_episode_link(
                    ep_id=selected_episode, movie_link=movie_result["base_link"]
                )

            # play the selected episode
            stream_movie(url=link_found)

        else:
            stream_movie(url=movie_result["link"])
    except Exception as e:
        raise Exception(f"{THEME['error']} {e}")


@app.command(help="A bit about me and Net-cli")
def about():
    info = """
    [bold red underline]About Me[/]

    [bold cyan]Hi, my name is Amit [/bold cyan]
    [italic]
    I am a college student who enjoys building tools like this.

    If you like what I built or want to share feedback,
    feel free to reach out to me.
    [/italic]

    [bold yellow]Email: <amitbhagat621@gmail.com>[/]

    [bold red underline]About Net-CLI[/]

    [italic]
    Net-CLI lets you watch movies and series directly from your terminal
    without opening websites or dealing with annoying pop-up ads.

    The goal of Net-CLI is simple:
    to remove the frustration and provide a clean,
    fast, and enjoyable watching experience.
    [/italic]

    [bold red underline]Other projects you might find useful[/]

    - File Host: [blue]https://infiniteamit.pythonanywhere.com[/]
    - Sub-Domain-Lender : [blue]https://subdomainlender.amit4218.fun[/]
    - Dns-lookup: [blue]https://dnslookup.amit4218.fun[/]
    - Google-maps-scraper: [blue]https://github.com/Amit4218/basic-maps-scraper[/]
    """
    CONSOLE.print(
        (Panel(info, title="[bold green]About me & Net-cli[/]", border_style="cyan"))
    )
