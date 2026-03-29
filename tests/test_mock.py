from playwright.sync_api import expect

def test_mock_data(browser):
    context = browser.new_context()
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    page = context.new_page()
    # 模拟返回数据
    def handle(route):
        route.fulfill(
            json = [{"name":"Strawberry","id":21}]
        )
    page.route("*/**/api/v1/fruits",handle)


    page.goto("https://demo.playwright.dev/api-mocking")
    expect(page.get_by_text("Strawberry")).to_be_visible()
    context.tracing.stop(path="trace.zip")
    context.close()


def test_mock_data_fetch(page):
    def handle(route):
        response = route.fetch()
        json = response.json()
        json.append({"name":"Loquat","id":100})
        route.fulfill(response= response,json = json)

    page.route("*/**/api/v1/fruits",handle)
    with page.expect_response("*/**/api/v1/fruits") as res:
        page.goto("https://demo.playwright.dev/api-mocking")

    print(f"返回数据:{res.value.json()}")
    expect(page.get_by_text("Loquat")).to_be_visible()

# def test_har_mock_true(page):
#     #将页面请求和响应信息存入fruit.har文件中
#     page.route_from_har("./hars/fruit.har",url="*/**/api/v1/fruits",update=True)
#
#     #启动页面
#     page.goto("https://demo.playwright.dev/api-mocking")
#
#     #验证请求拦截是否成功
#     expect(page.get_by_text("Strawberry")).to_be_visible()


def test_gets_the_json_from_har_and_checks_the_new_fruit_has_been_added(page):
    # Replay API requests from HAR.
    # Either use a matching response from the HAR,
    # or abort the request if nothing matches.
    page.route_from_har("./hars/fruit.har", url="*/**/api/v1/fruits", update=False)

    # Go to the page
    page.goto("https://demo.playwright.dev/api-mocking")

    # Assert that the Playwright fruit is visible
    expect(page.get_by_text("Playwright", exact=True)).to_be_visible()
