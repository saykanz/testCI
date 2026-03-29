# import os
#
# def test_download_report(page):
#     page.goto("http://localhost:3000")
#
#     with page.expect_download() as download_info:
#         page.get_by_role("button", name="下载报表").click()
#
#     download = download_info.value
#
#     file_path = "report.csv"
#     download.save_as(file_path)
#
#     # 1️⃣ 文件存在
#     assert os.path.exists(file_path)
#
#     # 2️⃣ 文件名
#     assert download.suggested_filename == "report.csv"
#
#     # 3️⃣ 文件内容
#     with open(file_path, encoding="utf-8") as f:
#         content = f.read()
#
#     assert "订单" in content
#
# def test_download_txt(page):
#     page.goto("http://localhost:3000")
#     with page.expect_download() as download_info:
#         page.get_by_role("button",name="下载").click()
#
#     download = download_info.value
#
#     download.save_as("text.txt")
#
#     assert os.path.exist("text.txt")
#
#     assert download.suggested_filename == "text.txt"
#
# import os
#
# def test_download_and_print(page):
#     # 1️⃣ mock 下载接口
#     page.route("**/api/download", lambda route: route.fulfill(
#         status=200,
#         headers={
#             "Content-Disposition": "attachment; filename=test.txt"
#         },
#         body="hello world"
#     ))
#
#     # 2️⃣ mock print（关键🔥）
#     page.add_init_script("""
#         window.__print_called = false;
#         window.print = () => {
#             window.__print_called = true;
#         };
#     """)
#
#     # 3️⃣ 打开页面
#     page.goto("http://localhost:3000")
#
#     # 4️⃣ 监听下载
#     with page.expect_download() as download_info:
#         page.get_by_role("button", name="下载").click()
#
#     download = download_info.value
#
#     file_path = "test.txt"
#     download.save_as(file_path)
#
#     # 5️⃣ 验证下载
#     assert os.path.exists(file_path)
#
#     with open(file_path, encoding="utf-8") as f:
#         content = f.read()
#
#     assert content == "hello world"
#
#     # 6️⃣ 验证 print（你问的重点🔥）
#     assert page.evaluate("window.__print_called") is True