import io
import subprocess

import requests
from PIL import Image as Img
from playwright.sync_api import Playwright, sync_playwright
from rich.align import Align
from rich.console import Console, Group
from rich.table import Table
from rich.text import Text
from textual_image.renderable import Image

SOAP_BASE_URL = ""  # save it in env


class ScrapeSoapToDay:
    def __init__(self, playwrite: Playwright) -> None:
        self._playwrite = playwrite
        self._browser = playwrite.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--incognito=new"],
        )
        self._context = self._browser.new_context()
        self._page = self._context.new_page()

        self._base_url = SOAP_BASE_URL
        self.session = requests.session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
                "Referer": self._base_url,
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            }
        )

    def _scrape_query_results(self) -> None:
        """Scrapes the website results based on what the user searched"""

        self._page.wait_for_selector("#resdata")

        cols = self._page.locator(".col")

        self.data = []

        for row in cols.all():
            title = row.locator("h3").text_content()
            image_link = row.locator("img").get_attribute("src")
            movie_link = row.locator("a").get_attribute("href")

            self.data.append(
                {
                    "title": title,
                    "image": image_link,
                    "movie_link": f"{self._base_url}{movie_link}",
                }
            )

        self._print_results(self.data)

    def _print_results(self, results: list[dict]) -> None:
        """Prints the query results to the console"""
        cell_width = 26
        console = Console()  # rich console to print image
        self.terminal_width = console.size.width
        self.result_columns = max(
            1, self.terminal_width // cell_width
        )  # max image in terminal column wise
        table = Table.grid(padding=1)  # table to display result
        row = []

        # create columns
        for _ in range(self.result_columns):
            table.add_column()

        for idx, result in enumerate(results):
            panel = self._image_helper(
                idx=idx, title=result["title"], req_image=result["image"]
            )

            row.append(panel)

            if len(row) == self.result_columns:
                table.add_row(*row)
                row = []

        if row:
            while len(row) < self.result_columns:
                row.append("")
            table.add_row(*row)

        console.print(table)

        self._get_selected_movie()  # take the user selection for the movie

    def _image_helper(self, idx: int, title: str, req_image: str) -> Group:
        """An helper method for _print_result to request image, resize and return it."""
        poster_size = max(
            80, min(150, (self.terminal_width // self.result_columns) * 6)
        )
        image_size = (poster_size, poster_size)

        try:
            res = self.session.get(req_image, timeout=5)

            if not res.status_code == 200:
                raise Exception("Image not found!")

            if "image" not in res.headers.get("content-type", ""):
                raise ValueError("Not an image")

            with Img.open(io.BytesIO(res.content)) as image:
                resized_img = image.resize(image_size, Img.Resampling.LANCZOS)

        except Exception:
            with Img.new("RGB", image_size, (40, 40, 40)) as image:
                resized_img = image.copy()

        img = Image(resized_img)

        title_text = Text(title, overflow="ellipsis", no_wrap=True)
        title_text.truncate(18)

        content = Group(
            Align.center(img),
            Align.center(Text(f"{idx}", style="bold cyan")),
            Align.center(title_text),
        )

        return content

    def _repeat(self):
        """Try to trigger player start without assuming specific UI"""
        selectors = [
            "#play-now",
            ".play-btn",
            "#play-btn",
            ".jw-icon-play",
            "button[title='Play']",
            "video",
            "iframe",
        ]

        for sel in selectors:
            try:
                el = self._page.locator(sel).first
                if el.is_visible(timeout=800):
                    el.click(timeout=800, force=True)
                    # print(f"Clicked {sel}")
                    return True
            except Exception:
                pass

        print("No clickable player element found, retrying...")
        return False

    def _block_popups(self, context, main_page):
        """An helper method to close new tabs which may <br>open when trying to click clicking the video player"""

        def handle_new_page(p):
            if p != main_page:
                # print("Blocked popup instantly")
                p.close()

        context.on("page", handle_new_page)

    def _get_selected_movie(self) -> None:

        max_click_attempts = 10  # max amount of click to do in the video player

        choice = input(
            "Enter (q or Quit) to exit:\n\nEnter the number of the movie: "
        ).strip()

        if choice.lower() == "q" or choice.lower == "quit":
            subprocess.run(["clear"])
            # print("Existing the application.....")
            exit()

        self._page.goto(
            f"{self.data[int(choice)]['movie_link']}#play-btn",
            wait_until="domcontentloaded",
        )

        self._block_popups(self._context, self._page)

        stream = self._capture_stream()

        while not stream["url"] and max_click_attempts > 0:
            max_click_attempts -= 1
            self._repeat()
            self._page.wait_for_timeout(5000)
            self._click_player()

        if stream["url"]:
            video_file = stream["url"]
            self._play_movie(video_file)
            self._browser.close()

    def _click_player(self) -> bool:
        """Simulate real user clicking the video"""

        try:
            iframe_element = self._page.wait_for_selector("iframe")
            frame = iframe_element

            if not frame:
                return False

            # print("Clicking inside player...")

            self._page.locator("#srv-1").click(force=True, timeout=5000)

            return True

        except Exception:
            # print("Player click failed")
            return False

    def _capture_stream(self):

        stream = {"url": None}

        def handle_response(response):
            url = response.url.lower()

            if any(x in url for x in [".m3u8", ".mp4", "master", "playlist"]):
                if response.status == 200:
                    # print("\nSTREAM FOUND:", response.url)
                    stream["url"] = response.url

        self._page.on("response", handle_response)

        return stream

    def _play_movie(self, m3u8_file: str) -> None:
        """Plays the movie using the mpv player with the .m3u8 url"""
        subprocess.run(["mpv", "--referrer=https://ployan.live", m3u8_file])

    def _download_movie(self) -> None:
        pass

    def _search_user_query(self, user_query: str) -> None:

        modified_user_query = user_query.strip().replace(" ", "+")

        self._page.goto(f"{self._base_url}/search/?q={modified_user_query}")

        self._scrape_query_results()


with sync_playwright() as playwrite:
    s = ScrapeSoapToDay(playwrite=playwrite)

    s._search_user_query("superman")

