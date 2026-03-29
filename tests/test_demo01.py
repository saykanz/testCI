import re
from playwright.sync_api import Page, expect,sync_playwright

# def test_has_title(page: Page):
#     page.goto("https://waer.ltd/")
#     expect(page).to_have_title(re.compile("Welight"))
#
#
# def test_get_started_link(page: Page):
#     page.goto("https://waer.ltd/")
#
#     # 直接点击（自带等待）
#     page.get_by_role("link", name="定价").click()
#
#     # 断言页面跳转成功
#     expect(page).to_have_url("https://waer.ltd/pricing")
#
# def test_sync(page):
#         page.goto("https://waer.ltd")
#         page.screenshot(path="screenshot/welight.png")
#
# def test_email_163(page):
#     page.goto("https://mail.163.com/")
#
#     # frame = page.frame_locator("#x-URS-iframe") 这种不行
#     # frame = page.frame_locator('//iframe[contains(@id, "x-URS-iframe")]') #这种可以
#     frame = page.frame_locator('iframe[id*="x-URS-iframe"]')#推荐这种
#
#     print("frame:", frame)
#     # 输入账号
#     frame.get_by_placeholder("邮箱账号或手机号码").fill("saykanz")
#
#     # frame.locator('input[type="password"][name="password"]').fill("geokjoerj")
#     # 或再加 class 保险
#     # frame.locator('input[type="password"].dlpwd').fill("geokjoerj")
#     frame.locator('input[type="password"].dlpwd').press_sequentially("syajkan")
#     # 勾选协议（如果需要）
#     frame.get_by_role("checkbox").check()
#
#     # 点击登录
#     # frame.locator("#dologin").click()  # 正确
#     # frame.get_by_text("登录").press("Enter")
#     frame.locator("#dologin").press("Enter")

def test_login_ali(page):
    page.goto("https://www.aliyundrive.com/sign/in", wait_until="networkidle")
    page.wait_for_timeout(2000)  # 让页面加载完动态内容

    # 尝试定位登录 iframe（多种常见写法，2026年主流）
    frame = None
    possible_iframe_selectors = [
        'iframe[src*="passport"]',
        'iframe[src*="sign"]',
        'iframe[src*="login"]',
        'iframe[title*="登录"]',
        'iframe[data-testid*="login"]',
        'iframe',  # 最坏情况：只有一个iframe就用它
    ]

    for sel in possible_iframe_selectors:
        try:
            f = page.frame_locator(sel)
            # 检查这个frame是否有可见内容
            if f.locator("body").is_visible(timeout=5000):
                frame = f
                print(f"使用 iframe selector: {sel}")
                break
        except:
            pass
    frame = frame.frame_locator("iframe[id='alibaba-login-box']")
    print("frame得值：",frame)

    if frame is None:
        print("没找到合适的 iframe → 假设登录在主页面")
        frame = page
        print("frame得值：", frame)
    # 步骤1: 切换到“账号登录” / “密码登录”模式
        # 优先用文本匹配（最稳）
    account_btn = frame.get_by_text("账号登录").or_(
        frame.get_by_text("密码登录")
    ).or_(
        frame.locator("div:has-text('账号')")
    ).or_(
         frame.locator("login-content")
    ).first
    account_btn.get_by_text("账号登录").click()
    print("account得值：",account_btn)
    # if account_btn.is_visible(timeout=8000):
    #         account_btn.click()
    #         print("已点击 '账号登录' 或 '密码登录'")
    #         page.wait_for_timeout(1500)
    # else:
    #         print("没找到账号登录按钮 → 可能默认就是，或已登录")

    # 步骤2: 填写账号（手机号/账号）
    try:
        account_input = frame.locator(
            'input[placeholder*="账号"], input[placeholder*="手机号"], '
            'input[type="text"], input[type="tel"], input[name="account"], '
            'input[autocomplete="username"]'
        ).first

        account_input.wait_for(state="visible", timeout=10000)
        account_input.fill("17366637245")
        print("已填写账号: 17366637245")
    except:
        print("账号输入框没找到！页面结构可能变了 → 截图看下")
        page.screenshot(path="account_input_failed.png")
        return

    # 步骤3: 填写密码
    try:
        pwd_input = frame.locator(
            'input[type="password"], input[placeholder*="密码"], '
            'input[name="password"], input[autocomplete="current-password"]'
        ).first

        pwd_input.fill("hpjy250406")
        print("已填写密码: hpjy250406")
    except:
        print("密码框没找到")
        return

    # 步骤4: 点击登录按钮
    try:
        submit_btn = frame.locator('button[type="submit"]').first

        submit_btn.click()
        print("已点击登录按钮")
    except:
        print("登录按钮没找到")
        page.screenshot(path="submit_failed.png")
        return

    # 步骤5: 等待结果（成功 or 失败提示）
    try:
        # 成功标志：跳转到 /drive 或出现“我的文件”等
        page.wait_for_url("**/drive", timeout=20000)
        print("登录成功！已跳转到网盘页面")
    except:
        # 失败常见：验证码、账号错、滑块
        error_msg = page.locator("text=验证码, text=错误, text=不存在, text=滑块").text_content(timeout=5000) or "未知错误"
        print(f"登录失败：{error_msg}")
        page.screenshot(path="login_result.png")

def test_profile_page(auth_page):
    # 直接访问需要登录的页面
    auth_page.goto("https://portal.qiniu.com/kodo/bucket/resource-v2?bucketName=tisox-blog-img&prefix=tests%2F")

    # 验证用户信息存在（说明已登录）
    expect(auth_page).to_have_url("https://portal.qiniu.com/kodo/bucket/resource-v2?bucketName=tisox-blog-img&prefix=tests%2F")