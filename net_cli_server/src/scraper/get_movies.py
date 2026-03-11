from typing import List

from playwright.sync_api import sync_playwright
from src.helpers.helpers import get_movie_urls


def scrape_movie_link(movie_link: str, head: bool = True):
    """Verify for movie and scrapes the movie playable
    <br> link, else returns the number of eps"""

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=head)
        context = browser.new_context()
        page = context.new_page()

        url = []

        context.on(
            "request",
            lambda resp: (
                url.append(resp.url) if "embos.net/movie" in resp.url else None
            ),
        )

        # go to the movie page
        page.goto(f"{movie_link}#play-now")

        # try to click the play-button
        while True:
            try:
                page.mouse.wheel(delta_x=0, delta_y=4)
                page.evaluate("document.querySelector('#play-now').click()")
                page.mouse.wheel(delta_x=0, delta_y=-4)
            except Exception:
                break

        # click the correct server button
        page.mouse.wheel(delta_x=0, delta_y=-4)
        page.get_by_role("button", name="Server 1").click()

        # check if its a movie or series
        ep_list = page.locator("#eps-list").locator("button").all()
        if len(ep_list) > 1:
            episode_ids: List[str | None] = [ep.get_attribute("id") for ep in ep_list]
            browser.close()
            data = {
                "movie": False,
                "message": "Please select an episode",
                "episodes": episode_ids,
                "base_link": movie_link,
            }
            return data

        # if its a movie
        src = page.locator("#playit").get_attribute("src")

        page.goto(str(src))
        page.wait_for_timeout(3000)
        browser.close()

        movie_id = url[0].split("=")[-1]
        languages_options = get_movie_urls(movie_id=movie_id)
        data = {
            "movie": True,
            "message": "Please select an language",
            "episodes": languages_options,
        }
        return data
