import os
import socket
import tempfile
import pytest
from pathlib import Path
from playwright.sync_api import Playwright, Browser, BrowserContext
import subprocess

# 更新后的执行文件路径
EXECUTABLE_PATH = Path("D:/softwares/Welight/welight.exe")

# 设置永久化的用户数据目录
USER_DATA_DIR = Path("D:/webview2_user_data")  # 修改为你希望存储用户数据的路径

# 创建目录，如果不存在则创建
if not USER_DATA_DIR.exists():
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)



@pytest.fixture(scope="session")
def webview2_process_cdp_port():
    cdp_port = _find_free_port()
    print("连接端口：", cdp_port)

    # 启动 WebView2 并使用持久化的用户数据文件夹（）
    process = subprocess.Popen(
        [EXECUTABLE_PATH],
        env={
            **dict(os.environ),
            "WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS": f"--remote-debugging-port={cdp_port}",
            "WEBVIEW2_USER_DATA_FOLDER": str(USER_DATA_DIR),  # 使用永久化的用户数据
        },
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        errors='ignore'  # 忽略解码错误
    )
    print("连接端口：", cdp_port)
    # 等待 WebView2 初始化完成
    while True:
        line = process.stdout.readline()
        print("连接端口line：", line)
        if "WebView2 initialized" in line:
            print("连接端口initisal：", cdp_port)
            break

    print("连接端口：",cdp_port)
    yield cdp_port
    process.terminate()

@pytest.fixture(scope="session")
def browser(playwright: Playwright, webview2_process_cdp_port: int):
    # 连接到通过 CDP 暴露的 WebView2 浏览器实例
    print("我是浏览器：")
    browser = playwright.chromium.connect_over_cdp(
        f"http://127.0.0.1:{webview2_process_cdp_port}"
    )
    print("连接端口ffffff：",webview2_process_cdp_port )
    print("我是浏览器：",browser)
    yield browser


@pytest.fixture(scope="session")
def context(browser):
    # 获取浏览器上下文
    context = browser.contexts[0]
    print("我是浏览器上下文：", context)
    yield context


@pytest.fixture(scope="session")
def page(context):
    # 获取浏览器页面
    page = context.pages[0]
    print("我是conftest中的page:",page)
    yield page


def _find_free_port(port=9000, max_port=65535):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(("", port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError("no free ports")