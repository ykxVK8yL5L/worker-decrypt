from cloakbrowser import launch
import argparse
import time
import sys

parser = argparse.ArgumentParser(description='Parse input data')
parser.add_argument("--url", help="Url to Browse", default="")
args = parser.parse_args()

TIMEOUT = 600       # 10分钟
INTERVAL = 5        # 5秒检查一次

if args.url:
    start = time.time()
    browser = launch()
    try:
        page = browser.new_page()
        print(f"打开页面: {args.url}")
        page.goto(
            args.url,
            wait_until="domcontentloaded",
            timeout=120000
        )
        while True:
            elapsed = time.time() - start
            # 超时
            if elapsed > TIMEOUT:
                print("失败: Hugging Face启动超过10分钟")
                sys.exit(1)
            try:
                title = page.title()
                url = page.url
            except Exception:
                title = ""
                url = ""

            print(
                f"[{elapsed:.0f}s] "
                f"title={title} "
                f"url={url}"
            )
            # 成功条件
            if (
                title
                and
                "Hugging Face – " not in title
            ):
                print("===================")
                print("启动成功")
                print("Title:", title)
                print("URL:", url)
                print(
                    f"耗时: {elapsed:.2f}s"
                )
                sys.exit(0)

            time.sleep(INTERVAL)
    except Exception as e:
        print("异常失败:", e)
        sys.exit(1)

    finally:

        browser.close()