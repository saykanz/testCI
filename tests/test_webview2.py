

import pytest
from playwright.sync_api import  expect


def test_webview2(context):
    page = context.new_page()
    print("嗯哼，我到了app")

    # 等待页面中出现 "welight" 文本
    page.wait_for_selector("text=Welight")  # 等待指定文本元素可见
    print("已经找到 Welight 文本")

    # 执行断言，确保 "welight" 文本可见
    expect(page.get_by_text("Welight")).to_be_visible()
    print("断言成功，'welight' 是可见的")