import pathlib
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parent.parent

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 420, "height": 900})
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))

    # Root landing page
    page.goto((root / "index.html").as_uri())
    assert page.locator("text=DAV6StudyBuddy").count() > 0
    page.screenshot(path=str(root / "scripts" / "nav_1_root.png"))

    # -> Maths
    page.click("a.subject-card.maths")
    page.wait_for_timeout(200)
    assert "maths_index.html" in page.url
    assert page.locator("text=Maths Buddy").count() > 0
    page.screenshot(path=str(root / "scripts" / "nav_2_maths_index.png"))

    # -> Chapter 1
    page.click('a[href="chapter1.html"]')
    page.wait_for_timeout(200)
    assert "chapter1.html" in page.url
    page.screenshot(path=str(root / "scripts" / "nav_3_chapter1.png"))

    # -> back to maths index
    page.click("text=← Chapters")
    page.wait_for_timeout(200)
    assert "maths_index.html" in page.url

    # -> back to root
    page.click("text=← DAV6StudyBuddy")
    page.wait_for_timeout(200)
    assert page.url.endswith("index.html") and "maths_index" not in page.url
    print("Maths path OK:", page.url)

    # -> Sanskrit
    page.click("a.subject-card.sanskrit")
    page.wait_for_timeout(200)
    assert "sanskrit_index.html" in page.url
    assert page.locator("text=Sanskrit Buddy").count() > 0
    page.screenshot(path=str(root / "scripts" / "nav_4_sanskrit_index.png"))

    # -> Sanskrit Chapter 1
    page.click('a[href="sanskrit1.html"]')
    page.wait_for_timeout(200)
    assert "sanskrit1.html" in page.url
    page.screenshot(path=str(root / "scripts" / "nav_5_sanskrit1.png"))

    # -> back to sanskrit index
    page.click("text=← Chapters")
    page.wait_for_timeout(200)
    assert "sanskrit_index.html" in page.url

    # -> back to root
    page.click("text=← DAV6StudyBuddy")
    page.wait_for_timeout(200)
    assert page.url.endswith("index.html") and "sanskrit_index" not in page.url
    print("Sanskrit path OK:", page.url)

    browser.close()

print("console/page errors across full flow:", errors)
print("FULL NAV FLOW PASSED" if not errors else "FAILED - ERRORS FOUND")
