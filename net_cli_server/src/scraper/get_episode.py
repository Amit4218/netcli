from playwright.sync_api import sync_playwright


def scrape_episode_link(ep_id, movie_link: str, head: bool = True):
    """gets the playable link for the series episode"""
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=head)
        context = browser.new_context()
        page = context.new_page()
        url = []

        # listen for the playable link request
        context.on(
            "request",
            lambda resp: url.append(resp.url) if ".m3u8" and "/hls/" in resp.url else None,
        )

        # go to he movie page
        page.goto(f"{movie_link}#play-now")

        # click the play-now button
        while True:
            try:
                page.mouse.wheel(delta_x=0, delta_y=4)
                page.evaluate("document.querySelector('#play-now').click()")
                page.mouse.wheel(delta_x=0, delta_y=-4)
            except Exception:
                break

        # select the Server
        page.mouse.wheel(delta_x=0, delta_y=-4)
        page.get_by_role("button", name="Server 1").click()

        # find the episodes
        ep_list = page.locator("#eps-list").locator("button").all()

        # click the episode button
        for ep in ep_list:
            if ep.get_attribute("id") == ep_id:
                ep.click()
                page.wait_for_timeout(2000)

        # goto the iframe src
        src = page.locator("#playit").get_attribute("src")
        page.goto(str(src))
        
        # wait for requests
        page.wait_for_timeout(3000)
        page.click
        
        # close browser and return playable link
        browser.close()
        return url[-1]


