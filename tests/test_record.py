from playwright.sync_api import expect

def test_record(browser):
    context = browser.new_context(
        record_video_dir="/vedios",
        record_video_size={"width":800,"height":400}
    )
    page = context.new_page()
    page.goto("https://mail.163.com/js6/main.jsp")