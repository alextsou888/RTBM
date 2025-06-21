from playwright.sync_api import sync_playwright

def test_bing_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 无头浏览器模式
        page = browser.new_page()

        # 打开 Bing 首页
        page.goto("https://www.bing.com")

        # 等待搜索框加载完成，最多等待 30 秒
        search_input_selector = "#sb_form_q"
        page.wait_for_selector(search_input_selector, timeout=30000)

        # 在搜索框中输入关键词
        page.fill(search_input_selector, "Playwright Python")

        # 模拟按下回车键，提交搜索
        page.press(search_input_selector, "Enter")

        # 等待搜索结果加载完成，最多等待 30 秒
        results_selector = "#b_results"
        page.wait_for_selector(results_selector, timeout=30000)

        # 简单断言：确认搜索结果区域存在
        assert page.query_selector(results_selector) is not None, "搜索结果未找到"

        browser.close()
