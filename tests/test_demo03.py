from playwright.sync_api import expect
def test_163_login_success(auth_page):
    print("auth_page的值：",auth_page)
    page = auth_page

    # 1. 进入邮箱首页 + 充分等待
    page.goto("https://mail.163.com/")


    # 2. 等待左侧导航栏加载（关键！）
    page.wait_for_selector('text=收件箱', timeout=10000)   # 先粗等
    page.wait_for_timeout(3000)
    print("当前页面 URL:", page.url)
    print("页面标题:", page.title())