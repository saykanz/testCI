# from datetime import datetime
# from playwright.sync_api import expect
#
# # 🧪 练习1：固定时间（基础必做🔥）
# # 🎯 场景
# #
# # 页面显示当前时间：
# # ✅ 要求
# # 固定时间为：2024-02-02 10:00:00
# # 验证页面显示正确时间
# def test_clock_fixed(page):
#     page.clock.set_fixed_time(datetime(2024,2,2,10,0,0))
#     page.goto("http://localhost:3000")
#     expect(page.get_by_test_id("time")).to_have_text("2/2/2024, 10:00:00 AM")
#
#
# # 🧪 练习2：倒计时（核心🔥）
# # 🎯 场景
# # <div id="countdown">5</div>
# # <script>
# #   let i = 5;
# #   setInterval(() => {
# #     i--;
# #     document.getElementById("countdown").innerText = i;
# #   }, 1000);
# # </script>
# # ✅ 要求
# # 启动页面
# # 快进 3 秒
# # 验证显示为 2
# def test_clock_fast_forward(page):
#     page.clock.install()
#     page.goto("http://localhost:3000")
#     page.clock.fast_forward("00:03")
#     expect(page.get_by_role("#countdown")).to_have_text("2/2/2024,10:00:03")
#
# #
# # 🧪 练习3：自动登出（企业高频🔥🔥🔥）
# # 🎯 场景
# # setTimeout(() => {
# #   document.body.innerText = "已自动退出";
# # }, 300000); // 5分钟
# # ✅ 要求
# # 不等待 5 分钟
# # 快进时间
# # 验证自动退出
# def test_clock_auto_logout(page):
#     page.clock.install()
#     page.goto("http://localhost:3000")
#     page.clock.fast_forward("05:00")
#     expect(page.get_by_text("已自动退出")).to_be_visible()
#
# # 🧪 练习4：精确时间推进（进阶🔥）
# # 🎯 场景
# #
# # 页面每秒更新时间
# #
# # ✅ 要求
# # 初始时间：10: 00:00
# # 推进
# # 2
# # 秒
# # 验证变成：10: 00:02
#
# def test_clock_prompt(page):
#     page.clock.install(datetime(2026,3,24,10,00,00))
#     page.goto("http://localhost:3000")
#     page.clock.run_for(2000)
#     expect(page.get_by_text()).to_have_text("3/24/2026,10:00:02 AM")
#
#
# # 🧪 练习5：暂停时间（高级🔥）
# # 🎯 场景
# #
# # 页面时间自动增长
# #
# # ✅ 要求
# # 暂停时间在 10:00:00
# # 等待（但时间不变）
# # 验证时间没有变化
# def test_clock_pause(page):
#     page.clock.intall()
#     page.clock.pause_at(datetime(2026,3,24,10,00,00))
#     page.goto("http://localhost:3000")
#     page.wait_for_timeout(10000)
#     expect(page.get_by_text("页面时间")).to_have_text("3/24/2026,10:00:10 AM")
#
# # 🧪 练习6：模拟活动时间（企业真实🔥）
# # 🎯 场景
# # if (new Date().getHours() >= 0) {
# #   document.body.innerText = "活动开始";
# # }
# # ✅ 要求
# # 模拟时间为凌晨 00:00
# # 验证活动开始
# def test_clock_settime(page):
#     page.clock.set_fixed_time(datetime(2024, 2, 2, 0, 0, 0))
#     page.goto("http://localhost:3000")
#     expect(page.get_by_text("活动开始")).to_be_visible()
#
# # 🧠 进阶练习（你必须尝试🔥）
# # 🧪 练习7（自己写）
# #
# # 👉 场景：
# #
# # 点击按钮 → 3秒后显示“成功”
# #
# # 要求：
# #
# # 不用 sleep
# # 用 clock 直接触发
# def test_clock_button(page):
#     page.clock.install()
#     page.goto("http://localhost:3000")
#     page.get_by_role("button").click()
#     page.clock.fast_forward(3000)
#     expect(page.get_by_text("成功")).to_be_visible()