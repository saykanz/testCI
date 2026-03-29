# from playwright.sync_api import sync_playwright
import pytest
def run(playwright):
    iphone_13 = playwright.devices['iPhone 13']

    browser = playwright.webkit.launch(headless=False)

    context = browser.new_context(**iphone_13)

    page = context.new_page()

    page.goto("https://www.baidu.com",timeout=5000)

    print(page.title())

    browser.close()

# with sync_playwright() as playwright:
#     run(playwright)


#项目写法
@pytest.fixture(params=[
    ("Desktop", None, "chromium"),
    ("iPhone 13", "iPhone 13", "webkit"),
])
def device_context(playwright, request):
    name, device, browser_name = request.param

    browser = getattr(playwright, browser_name).launch(headless=False)

    if device:
        context = browser.new_context(**playwright.devices[device])
    else:
        context = browser.new_context()

    yield context

    context.close()
    browser.close()