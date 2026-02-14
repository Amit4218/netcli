import io
import subprocess
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qs, unquote, urlparse

import requests
from PIL import Image as Img
from playwright.sync_api import Playwright, sync_playwright
from rich.align import Align
from rich.console import Console, Group
from rich.table import Table
from rich.text import Text
from textual_image.renderable import Image

SOAP_BASE_URL = "https://ww3.soap2dayhdz.com"  # put in env
MODERN_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36"


class SoapScraper:
    def __init__(self, playwright: Playwright):
        self.playwright = playwright
        self.browser = playwright.chromium.launch(headless=True, args=["--incognito"])
        self.context = self.browser.new_context(user_agent=MODERN_UA)
        self.page = self.context.new_page()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": MODERN_UA})
        self._block_popups()

    def _block_popups(self):
        """helper to close new tabs if opened"""

        def handler(p):
            if p != self.page:
                p.close()

        self.context.on("page", handler)

    def search(self, query: str):
        """searches the user query"""
        q = query.strip().replace(" ", "+")
        self.page.goto(f"{SOAP_BASE_URL}/search/?q={q}")
        self.page.locator("#resdata")

        results = []
        for row in self.page.locator(".col").all():
            results.append(
                {
                    "title": row.locator("h3").text_content(),
                    "image": row.locator("img").get_attribute("src"),
                    "link": SOAP_BASE_URL + row.locator("a").get_attribute("href"),  # pyright: ignore[reportOperatorIssue]
                }
            )

        self._render_results(results)

    def _fetch_image(self, url, size):
        """helper to request images and resize it to display in the terminal"""
        try:
            r = self.session.get(url, timeout=5)
            if r.ok and "image" in r.headers.get("content-type", ""):
                img = Img.open(io.BytesIO(r.content)).resize(
                    size, Img.Resampling.LANCZOS
                )
                return img
        except Exception:
            pass
        return Img.new("RGB", size, (40, 40, 40))

    def _render_results(self, results):
        """displays the search results in a nice format using rich"""
        console = Console()
        width = console.size.width
        cols = max(1, width // 26)
        table = Table.grid(padding=1)

        for _ in range(cols):
            table.add_column()

        poster = (90, 90)

        with ThreadPoolExecutor(max_workers=8) as ex:
            images = list(
                ex.map(lambda r: self._fetch_image(r["image"], poster), results)
            )

        row = []
        for i, (data, img) in enumerate(zip(results, images)):
            panel = Group(
                Align.center(Image(img)),
                Align.center(Text(str(i), style="bold cyan")),
                Align.center(Text(data["title"], overflow="ellipsis", no_wrap=True)),
            )
            row.append(panel)
            if len(row) == cols:
                table.add_row(*row)
                row = []

        if row:
            while len(row) < cols:
                row.append("")
            table.add_row(*row)

        console.print(table)
        self._choose(results)

    def _wait_stream(self):
        """listens to the network stream for potential data containing urls"""
        try:
            with self.page.expect_response(
                lambda r: any(
                    x in r.url.lower() for x in (".m3u8", ".mp4", "playlist", "master")
                ),
                timeout=20000,
            ) as resp_info:
                pass
            return resp_info.value.url
        except Exception:
            return None

    def _play(self, url: str):
        """plays the movie once the stream link is found"""
        subprocess.run(["mpv", "--referrer=https://ployan.live", url])

    def _url_parser(self, dirty_url):
        """helper to parse dirty_url that might contain browser encoded and extra params"""
        query = urlparse(dirty_url).query
        params = parse_qs(query)
        m3u8 = unquote(params["mu"][0])
        return m3u8

    def _is_dirty_url(self, url) -> bool:
        """helper to determine if its a dirty_url"""
        return "jwpltx.com" in url and "ping.gif" in url and "mu=" in url

    def _choose(self, results):
        """prompts the user to choose a movie from the displayd results and fetches the stream url"""
        choice = input("Select movie (q to quit): ").strip().lower()
        if choice in ("q", "quit"):
            self.browser.close()
            return

        try:
            idx = int(choice)
            movie = results[idx]
        except Exception:
            print("Invalid selection")
            return self._choose(results)

        self.page.goto(f"{movie['link']}")

        self.page.wait_for_timeout(5000)

        for _ in range(500):
            self.page.mouse.down()

        self.page.evaluate("document.getElementById('play-now').click()")

        self.page.on("popup", lambda r: self._block_popups())

        self.page.wait_for_timeout(2000)

        self.page.evaluate("document.getElementById('srv-1').click()")

        stream = self._wait_stream()

        if not stream:
            print("No stream detected")

        if self._is_dirty_url(stream):
            stream = self._url_parser(stream)

        self.browser.close()
        self._play(stream)  # type: ignore

    @staticmethod
    def start(query) -> None:
        with sync_playwright() as playwrite:
            soap = SoapScraper(playwright=playwrite)
            soap.search(query)


def start_soap_scraper(user_query) -> None:
    SoapScraper.start(query=user_query)
