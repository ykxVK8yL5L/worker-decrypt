from cloakbrowser import launch
import argparse

parser = argparse.ArgumentParser(description='Parse user data')
parser.add_argument("--email", help="Login Email", default="")
parser.add_argument("--password", help="Login Password", default="")
args = parser.parse_args()

if args.email:
    browser = launch()
    page = browser.new_page()
    page.goto("https://iios.fun")
    # 定位输入框并输入邮箱
    email_input = page.locator('input[placeholder="请输入邮箱"]')
    if email_input.is_visible():
        email_input.fill(args.email)
        # 定位输入框并输入密码
        password_input = page.locator('input[placeholder="请输入密码"]')
        password_input.fill(args.password)
        # 点击登录并等待页面跳转
        with page.expect_navigation():
            page.get_by_text("提交登录").click()

    page.locator("text=个人中心").wait_for(state="visible")
    page.goto("https://www.iios.fun/#/points")
    page.locator("text=每日签到").wait_for(state="visible")
    page.wait_for_timeout(5000)  # 等待5秒以捕获请求和响应
    if page.locator("text=已完成").count() > 0:
        print("签到已完成，结束操作")
    # 判断是否有“立即签到”按钮
    elif page.locator("text=立即签到").count() > 0:
        print("发现立即签到按钮，点击签到")
        page.locator("text=立即签到").click()
    else:
        print("没有签到相关元素")
    browser.close()



 



