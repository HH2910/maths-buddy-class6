import pathlib
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parent.parent

def check_page(page, url, name):
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(url)
    page.wait_for_timeout(300)
    return errors

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 420, "height": 900})

    # Index
    errs = check_page(page, (root / "sanskrit_index.html").as_uri(), "index")
    page.screenshot(path=str(root / "scripts" / "shot_index.png"))
    print("index errors:", errs)
    assert page.locator("text=Sanskrit Buddy").count() > 0

    for ch in (1, 2):
        errs = check_page(page, (root / f"sanskrit{ch}.html").as_uri(), f"ch{ch}")
        print(f"ch{ch} errors:", errs)
        # section tabs present
        tabs = page.locator(".sec-btn")
        n = tabs.count()
        print(f"ch{ch} section tabs:", n)
        assert n > 0
        # question text visible
        qtext = page.locator("#q-text").inner_text()
        print(f"ch{ch} first question:", qtext[:60])
        page.screenshot(path=str(root / "scripts" / f"shot_ch{ch}_q1.png"))

        # click show answer
        page.click("#show-btn")
        page.wait_for_timeout(150)
        visible = page.locator("#answer-box.visible").count()
        print(f"ch{ch} answer visible after click:", visible > 0)
        page.screenshot(path=str(root / "scripts" / f"shot_ch{ch}_answer.png"))

        # click through section tabs
        for i in range(n):
            tabs.nth(i).click()
            page.wait_for_timeout(100)
        print(f"ch{ch} clicked through {n} tabs OK")

        # next question nav
        page.click(".sec-btn >> nth=0")
        page.click("#next-btn")
        page.wait_for_timeout(150)
        qtext2 = page.locator("#q-text").inner_text()
        print(f"ch{ch} second question:", qtext2[:60])

    browser.close()

print("ALL CHECKS PASSED")
