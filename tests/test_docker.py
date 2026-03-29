def test_demo(page):
    # 1️⃣ 打开网页
    page.goto("https://example.com")

    # 2️⃣ 打印标题（调试用）
    print(page.title())

    # 3️⃣ 断言页面标题
    assert "Example" in page.title()