from playwright.sync_api import expect, Page

def test_snap_expect(auth_page):
    page: Page = auth_page
    page.pause()
    # 确保进入真正的邮箱主界面（避免停在欢迎页）
    print("正在进入 163 邮箱主界面...")
    page.goto("https://mail.163.com/js6/main.jsp", wait_until="networkidle")
    page.wait_for_load_state("networkidle", timeout=20000)

    # 等待左侧导航树加载完成
    tree_locator = page.locator("#_mail_tree_0_104")

    tree_locator.wait_for(timeout=15000)
    actual_snapshot = tree_locator.aria_snapshot()
    print(actual_snapshot)

    # 基础验证：首页标签存在
    expect(page.get_by_text("首页")).to_be_visible(timeout=10000)

    # ==================== 推荐的 ARIA Snapshot（更稳定版） ====================
    expect(tree_locator).to_match_aria_snapshot("""
- tree "左侧导航":
  - treeitem "收件箱(78)":
    - treeitem "收件箱(78)":
      - text: 收件箱
      - strong: (78)
  - treeitem "红旗邮件":
    - treeitem "红旗邮件"
  - treeitem "待办邮件":
    - treeitem "待办邮件"
  - treeitem "智能标签":
    - treeitem "智能标签"
  - treeitem "星标联系人邮件":
    - treeitem "星标联系人邮件"
  - treeitem "草稿箱":
    - treeitem "草稿箱"
  - treeitem "已发送":
    - treeitem "已发送"
  - treeitem "其他3个文件夹 左侧导航":
    - treeitem "其他3个文件夹":
      - text: 其他3个文件夹
      - strong
    - tree "左侧导航"
  - treeitem "邮件标签 左侧导航":
    - treeitem "邮件标签":
      - text: 邮件标签
      - strong
    - tree "左侧导航"
  - treeitem "邮箱中心 左侧导航":
    - treeitem "邮箱中心":
      - text: 邮箱中心
      - strong
    - tree "左侧导航"
  - treeitem "超大附件":
    - treeitem "超大附件"
  - treeitem "邮箱附件":
    - treeitem "邮箱附件"
  - listitem:
    - text: 其他工具
    - img
    - text: 邮件追踪 简历优化 智能面试顾问 求职信息订阅
    - img
    - text: PDF转换工具
    - img
    - text: 发票助手
    - img
    - img
    - text: 企业邮箱

    """)

    print("✅ ARIA Snapshot 验证通过！左侧导航结构正确。")