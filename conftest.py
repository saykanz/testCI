import pytest
import os
from playwright.sync_api import expect

@pytest.fixture(scope="session")
def storage_state(browser):
    if os.path.exists("state.json"):
        print("复用已有登录态")
        return "state.json"

    #创建一个无状态的模拟框
    context = browser.new_context()
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    page = context.new_page()

    page.goto("https://mail.163.com/",wait_until="networkidle")

    targets = [page] + page.frames

    logged = False
    for f in targets:
        try:
            phone = f.get_by_role("textbox", name="邮箱账号或手机号码")
            if phone.is_visible(timeout=5000):
                print("找到登录框，开始登录...")
                phone.fill("saykanz")
                # page.pause()
                f.locator('input[type="password"][name="password"]').fill("0408@Zfang")
                f.get_by_text("天内免登录").check()
                f.get_by_role("link", name="登  录").click()
                print("等待跳转路劲")
                # f.wait_for_timeout(10000)
                expect(page.locator('span[title="草稿箱"]')).to_be_visible(
                    timeout=15000
                )  # 可行
                # f.wait_for_load_state("networkidle", timeout=10000)
                print("============登录成功！！！！==================")
                logged = True
                context.storage_state(path="state.json")
                context.tracing.stop(path="trace.zip")
                break
        except Exception as e:
            print("错误信息：",e)
            continue

    if not logged:
        print("登录失败")
    context.close()

    return "state.json"

@pytest.fixture
def auth_page(browser,storage_state):
    print("storage_state的值:",storage_state)
    context = browser.new_context(storage_state=storage_state)
    page = context.new_page()
    yield page
    context.close()

