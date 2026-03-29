import pytest
from playwright.sync_api import sync_playwright
#定义视口大小
@pytest.fixture(scope="session")
def browser_context_viewport(browser_context_args):
    return {
        "viewport":{
            "width":1920,
            "height":1080
        }
    }


#设备模拟
@pytest.fixture(scope="session")
def browser_context_device(browser_context_args, playwright):
    iphone_11 = playwright.devices['iPhone 11 Pro']
    return {
        **browser_context_args,
        **iphone_11,
    }

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def storage_state(browser):
    """只执行一次：登录并保存状态"""
    context = browser.new_context()
    page = context.new_page()
        # 1. 打开登录页
    page.goto("https://sso.qiniu.com/",wait_until="networkidle")

        # 2. 执行登录
    #     page.goto(
    #     "https://portal.qiniu.com/kodo/bucket/resource-v2?bucketName=tisox-blog-img&prefix=tests%2F",
    #     wait_until="networkidle"
    # )

    # 等待页面加载完成（七牛云登录通常在 iframe 中）
    page.wait_for_timeout(3000)

    # 遍历所有 frame（包括主页面）
    targets = [page] + page.frames

    logged_in = False

    for f in targets:
        try:
            # 查找登录输入框（邮箱/手机号）
            phone_locator = f.get_by_placeholder("邮箱 / 手机号（海外手机号格式: +xxxxx）")

            if phone_locator.is_visible(timeout=5000):
                print("找到登录框，开始登录...")

                phone_locator.fill("17366637245")
                f.get_by_placeholder("请输入密码").fill("5247xuyi")

                # 点击登录按钮
                f.get_by_role("button", name="登录").click()

                # 等待登录成功（可根据实际情况调整）
                page.wait_for_timeout(8000)
                print("登录成功！！！！")
                logged_in = True
                # 3. 等待登录成功（必须有！）
                page.wait_for_url("https://portal.qiniu.com/home")
                # 4. 保存登录态
                context.storage_state(path="state.json")
                break

        except Exception as e:
            # print(f"当前 frame 尝试失败: {e}")  # 调试时可打开
            continue

    if not logged_in:
        print("未找到登录框或登录失败")
        return




    return "state.json"


@pytest.fixture
def auth_page(browser, storage_state):
    """每个测试用例都会使用已登录的页面"""

    context = browser.new_context(storage_state=storage_state)
    page = context.new_page()

    yield page

    context.close()