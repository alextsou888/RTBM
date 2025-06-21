import pytest
from playwright.sync_api import sync_playwright

def test_google_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 无头浏览器
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.fill("input[name='q']", "Playwright Python")
        page.press("input[name='q']", "Enter")
        page.wait_for_selector("text=Playwright")
        assert "Playwright" in page.content()
        browser.close()
