from playwright.sync_api import sync_playwright
from src.helpers.helpers import get_episode_url


def scrape_episode_link(ep_id, movie_link: str, head: bool = True):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=head)
        context = browser.new_context()
        page = context.new_page()
        url = []

        context.on(
            "request",
            lambda resp: print(resp.url) if ".m3u8" in resp.url else None,
        )

        # go to he movie page
        page.goto(f"{movie_link}#play-now")

        while True:
            try:
                page.mouse.wheel(delta_x=0, delta_y=4)
                page.evaluate("document.querySelector('#play-now').click()")
                page.mouse.wheel(delta_x=0, delta_y=-4)
            except Exception:
                break

        page.mouse.wheel(delta_x=0, delta_y=-4)
        page.get_by_role("button", name="Server 1").click()

        ep_list = page.locator("#eps-list").locator("button").all()

        # click the episode button
        for ep in ep_list:
            if ep.get_attribute("id") == ep_id:
                ep.click()
                page.wait_for_timeout(2000)

        src = page.locator("#playit").get_attribute("src")
        page.goto(str(src))
        page.wait_for_timeout(5000)
        page.click
        browser.close()
        print(url[-1])
        data = get_episode_url(link=url[-1])
        return data


# print(
#     scrape_episode_link(
#         "ep-1",
#         "https://ww3.soap2dayhdz.com/film/my-adventures-with-superman-season-1-1630855431",
#         False,
#     )
# )
