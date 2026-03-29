import pytest
from datetime import datetime
from playwright.sync_api import expect

def test_print(page):
    page.add_init_script("""
            window.__print_called = false;
            window.print = () => {
                window.__print_called = true;
            };
        """)
    page.goto()
    page.get_by_role("button",name="打印").clock()
    expect(page.evaluate("window.__print_called")).to_be_truthy()

from datetime import datetime


def test_mock_clock(page):
    # 1️⃣ 安装 clock（必须最先）
    page.clock.install(time=datetime(2026, 3, 24, 10, 0, 0))

    # 2️⃣ 提前注入 print mock
    page.add_init_script("""
        window.__print_called = false;
        window.print = () => {
            window.__print_called = true;
        };
    """)

    # 3️⃣ 打开页面
    page.goto("http://localhost:3000")

    # 4️⃣ 点击按钮
    page.get_by_role("button", name="打印").click()

    # 5️⃣ 快进时间
    page.clock.fast_forward("00:03")

    # 6️⃣ 验证 print
    assert page.evaluate("window.__print_called") is True

    # 7️⃣ 验证时间
    expect(page.get_by_text("页面时间")).to_have_text(
        "3/24/2026, 10:00:03 AM"
    )

from playwright.sync_api import expect

def test_print_after_api(page):
    # mock API
    page.route("**/api/print", lambda route: route.fulfill(
        status=200,
        body='{"success": true}'
    ))

    # 监听 print
    page.evaluate("""
        window.__print_called = false;
        window.print = () => {
            window.__print_called = true;
        };
    """)

    page.goto("http://localhost:3000")

    # 等接口返回
    with page.expect_response("**/api/print") as res:
        page.get_by_role("button", name="打印").click()

    assert res.value.status == 200

    # 再验证 print
    assert page.evaluate("window.__print_called") is True