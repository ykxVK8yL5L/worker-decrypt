from cloakbrowser import launch
import argparse
import time
import sys

parser = argparse.ArgumentParser(description='Parse input data')
parser.add_argument("--url", help="Url to Browse", default="")
args = parser.parse_args()

MAX_TIMEOUT = 600  # 最大执行时间 10分钟
CHECK_INTERVAL = 5  # 每5秒检查一次

if args.url:
    start_time = time.time()
    browser = launch()
    try:
        page = browser.new_page()
        page.goto(args.url)

        while True:
            elapsed = time.time() - start_time
            
            # 超时判断
            if elapsed >= MAX_TIMEOUT:
                print(f"失败: 超过最大执行时间 {MAX_TIMEOUT} 秒")
                print(f"总耗时: {elapsed:.2f} 秒")
                sys.exit(1)

            # 获取title
            title = page.title()

            print(f"当前title: {title}")
            print(f"已运行: {elapsed:.2f} 秒")

            # 判断title是否符合要求
            if "Hugging Face – " not in title:
                print("成功: 页面title已变化")
                print(f"最终title: {title}")
                print(f"执行耗时: {elapsed:.2f} 秒")
                sys.exit(0)

            # 等待后继续检查
            time.sleep(CHECK_INTERVAL)

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"失败: {str(e)}")
        print(f"执行耗时: {elapsed:.2f} 秒")
        sys.exit(1)

    finally:
        browser.close()