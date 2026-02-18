import time
from urllib.parse import parse_qs, unquote, urlparse

from playwright.sync_api import sync_playwright

from ..utils.helpers import (
    clear_screen,
    get_stream,
    save_history,
    search_helper,
    start_player,
    print_adaptive_grid
)
from ..utils.contants import FIREFOX_CONFIG,SOAP_BASE_URL,SOAP_IMAGE_PREFIX


class SoapScraper:
    def __init__(self, headless) -> None:
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(
            headless=headless, firefox_user_prefs=FIREFOX_CONFIG
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.main_page = self.page  # to keep track of the main tab

        self._setup_listners()

    def _setup_listners(self) -> None:
        """adds event listners to avoid new tab open and redirects"""
        self.context.on("page", self._block_new_tabs)
        self.page.on("framenavigated", self._prevent_redirect)

    def _prevent_redirect(self, frame):
        if frame != self.main_page.main_frame:
            return

        url = frame.url

        if url.startswith("about:"):
            return

    def _block_new_tabs(self, new_page) -> None:
        """closes new tabs if opened"""
        if new_page != self.main_page:
            # print("[Blocked popup]", new_page.url)
            try:
                new_page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass
            new_page.close()

    def _url_parser(self, dirty_url: str):
        """parse dirty_url that might contain browser encoded and extra params"""
        try:
            blocklist = [
                "ping.gif",
                "mu=",
                "prd.jwpltx.com",
                "jwplayer6",
            ]

            if any(x in dirty_url for x in blocklist):
                query = urlparse(dirty_url).query
                params = parse_qs(query)
                m3u8 = unquote(params["mu"][0])
                return m3u8

        except Exception:
            return dirty_url

    def _save_movies(
        self, query, title, type, stream_url, base_link, episode=None
    ) -> None:
        """helps save the movie to the history"""
        if episode and type == "series":
            data = {
                "type": type,
                "title": title,
                "user_query": query,
                "metadata": {f"{episode}": f"{stream_url}"},
                "base_link": base_link,
            }
        else:
            data = {
                "type": type,
                "title": title,
                "user_query": query,
                "metadata": {"link": f"{stream_url}"},
                "base_link": base_link,
            }

        save_history(data)

    def _scrape_series_episodes(self, id):
        """scrapes the episode links if the selected is not a movie"""
        try:
            time.sleep(3)

            while True:
                try:
                    self.page.evaluate("document.querySelector('#play-now').click()")
                    if self.page != self.main_page:
                        self.page.close()
                except Exception:
                    break

            self.page.locator("#srv-1").click()
            self.page.locator(f"{'#'}{id}").click()
            self.page.wait_for_timeout(3000)
            src = self.page.locator("#playit").get_attribute("src")
            if src:
                with self.page.expect_response(get_stream, timeout=20000) as resp:
                    self.page.goto(src)
                    stream = resp.value.url
                    url = self._url_parser(stream)
                    return url

        except Exception:
            return None

    def _scrape_movie_link(self):
        """returns the streamable movie file"""
        try:
            while True:
                try:
                    self.page.evaluate("document.querySelector('#play-now').click()")
                except Exception:
                    break

            with self.page.expect_response(get_stream, timeout=20000) as resp:
                self.page.locator("#srv-1").click()

                self.page.mouse.move(200, 200)
                self.page.mouse.down()
                self.page.mouse.up()

                self.page.keyboard.press("Space")

                stream = resp.value.url
                url = self._url_parser(stream)
                return url
        except Exception:
            return None

    def _search_query(self, user_query) -> dict | None:
        """searches and scrapes the user_query results"""
        search_results = []

        query = user_query.strip().replace(" ", "+")

        with self.page.expect_response(search_helper) as response_info:
            self.page.goto(f"{SOAP_BASE_URL}/search/?q={query}")

        if not response_info.value.json()["data"]:
            print("\nNo Results Found\n")
            return

        for movie in response_info.value.json()["data"]:
            search_results.append(
                {
                    "title": movie["t"],
                    "image": f"{SOAP_IMAGE_PREFIX}{movie['s']}.jpg",
                    "link": f"{SOAP_BASE_URL}/film/{movie['s']}",
                }
            )

        titles = [f"[{i + 1}] {r['title']}" for i, r in enumerate(search_results)]
        print_adaptive_grid(titles)
        movie_info = self._take_user_input(results=search_results)
        return movie_info

    def _take_user_input(self, results, slug="movie"):
        while True:
            choice = input(f"Select {slug} number (or q to quit): ").strip().lower()

            if choice == "q":
                print("Exiting...")
                self.quit()
                return None

            if not choice.isdigit():
                print("Please enter a valid number.")
                continue

            idx = int(choice) - 1

            if 0 <= idx < len(results):
                return results[idx]
            else:
                print("Please enter a valid number.")

    def _verify_movie_or_series(self, movie):
        """checks if its movie or series and scrapes accordingly"""
        self.page.goto(f"{movie}#play-now")
        ep_list = self.page.locator("#eps-list").locator("button").all()
        self.page.evaluate("document.querySelector('#play-now').click()")

        if len(ep_list) > 1:
            episode_ids = [ep.get_attribute("id") for ep in ep_list]
            items = [
                f"[{idx + 1}] {ep.get_attribute('id')}"
                for idx, ep in enumerate(ep_list)
            ]
            print_adaptive_grid(items=items)
            episode_id = self._take_user_input(results=episode_ids, slug="epidsode")

            episode_url = self._scrape_series_episodes(id=episode_id)

            return (episode_id, episode_url)

        movie_url = self._scrape_movie_link()
        return None, movie_url

    def quit(self) -> None:
        """stops the playwright and browser instances"""
        if self.browser and self.playwright:
            self.browser.close()
            self.playwright.stop()
            self.browser = None
            self.playwright = None

    def start(self, user_query) -> None:
        """"""
        try:
            movie_info = self._search_query(user_query)
            if movie_info:
                print(f"\nYou selected: {movie_info['title']}\n")
                episode_id, stream_url = self._verify_movie_or_series(
                    movie_info["link"]
                )

                if episode_id and stream_url:
                    print(f"\tNow playing {movie_info['title']}....")
                    self.quit()
                    # save to history
                    self._save_movies(
                        query=user_query,
                        title=movie_info["title"],
                        type="series",
                        stream_url=stream_url,
                        base_link=movie_info["link"],
                        episode=episode_id,
                    )
                    start_player(stream_url)

                if not episode_id and stream_url:
                    print(f"\tNow playing {movie_info['title']}....")
                    # save to history
                    self.quit()
                    self._save_movies(
                        query=user_query,
                        title=movie_info["title"],
                        type="movie",
                        stream_url=stream_url,
                        base_link=movie_info["link"],
                    )
                    start_player(stream_url)

        except Exception as err:
            clear_screen()
            print(err)
            self.quit()

        finally:
            clear_screen()
            self.quit()


def start_soap_scraper():
    scraper = SoapScraper(headless=True)
    clear_screen()
    user_query = input("Enter the movie / series name: ").strip().lower()
    scraper.start(user_query)
