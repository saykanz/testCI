# def test_login_ali(page):
#     page.goto("https://www.aliyundrive.com/sign/in", wait_until="networkidle")
#     page.wait_for_timeout(2000)  # 让页面加载完动态内容
#
#     found = False
#
#     for i,f in enumerate(page.frames):
#         link = f.locator('a:has-text("账号登录")')
#         if link.count()>0:
#             link.first.click()
#             found = True
#     if not found:
#         page.locator("a:has-text('账号登录')").click()
#
#     for f in page.frames:
#         try:
#             phone = f.get_by_placeholder("请输入手机号码")
#             if phone.count() > 0:
#                 phone.fill("17366637245")
#                 f.get_by_placeholder("请输入密码").fill("hpjy250406")
#                 f.get_by_role("button", name="登录").click()
#                 break
#         except:
#             continue


from playwright.sync_api import Page, expect,sync_playwright


def test_qiliuyun(page: Page):
    page.goto(
        "https://portal.qiniu.com/kodo/bucket/resource-v2?bucketName=tisox-blog-img&prefix=tests%2F",
        wait_until="networkidle"
    )

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
                break

        except Exception as e:
            # print(f"当前 frame 尝试失败: {e}")  # 调试时可打开
            continue

    if not logged_in:
        print("未找到登录框或登录失败")
        return

    # ==================== 文件上传部分 ====================

    # 再次遍历 frame（登录后页面可能刷新，frame 可能变化）
    targets = [page] + page.frames

    print("第二次target:",targets)

    for f in targets:
        try:
            # 找到“选择文件”按钮
            f.wait_for_timeout(5000)
            f.get_by_role("button", name="图标: upload 上传文件").click()
            upload_select_btn =f.locator('button[name="portalKodo@resourceV2-upload-select-files"]')

            if upload_select_btn.is_visible(timeout=5000):
                print("找到上传按钮，开始上传文件...")

                # 关键：先启动 expect_file_chooser，再点击按钮
                with f.expect_file_chooser() as fc_info:
                    upload_select_btn.click()

                file_chooser = fc_info.value
                file_chooser.set_files(r"D:\pythonItems\playwright\item01\account_input_failed.png")

                # 点击“开始上传”
                f.locator('button[name="portalKodo@resourceV2-upload-start"]').click()

                # 等待上传完成（可根据实际情况加更精确的等待）
                page.wait_for_timeout(10000)

                # 关闭可能出现的弹窗
                close_btn = f.locator(".ant-modal-close")
                if close_btn.is_visible(timeout=3000):
                    close_btn.click()

                # 刷新列表
                f.locator('button[name="portalKodo@resourceV2-refresh"]').click()

                print("图片上传完成！")
                break

        except Exception as e:
            # print(f"上传环节 frame 尝试失败: {e}")
            continue
    else:
        print("未找到上传按钮，上传失败")








