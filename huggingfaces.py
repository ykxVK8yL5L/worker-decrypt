from cloakbrowser import launch
import time
import sys
import os


TIMEOUT = 900       # 15分钟
INTERVAL = 5        # 5秒


# 从 GitHub Actions Secrets 获取
urls_env = os.environ.get("HF_URLS", "")


if not urls_env:
    print("错误: 没有配置 HF_URLS")
    sys.exit(1)


# 逗号分割
urls = [
    url.strip()
    for url in urls_env.split(",")
    if url.strip()
]


print("需要保活 URLs:")
for url in urls:
    print("-", url)



start = time.time()

browser = launch()


pages = {}


try:

    # 打开所有页面
    for url in urls:

        page = browser.new_page()

        print(f"打开页面: {url}")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=120000
        )

        pages[url] = {
            "page": page,
            "success": False
        }



    while True:

        elapsed = time.time() - start


        if elapsed > TIMEOUT:

            print(
                "失败: Hugging Face启动超过10分钟"
            )

            for url, info in pages.items():

                if not info["success"]:
                    print(
                        "未启动:",
                        url
                    )

            sys.exit(1)



        all_success = True



        for url, info in pages.items():


            if info["success"]:
                continue


            page = info["page"]


            try:

                title = page.title()
                current_url = page.url


            except Exception:

                title = ""
                current_url = ""



            print(
                f"[{elapsed:.0f}s]"
                f" {url}"
                f" title={title}"
            )



            if (
                title
                and
                "Hugging Face – " not in title
            ):

                info["success"] = True

                print(
                    "启动成功:",
                    url
                )


            else:

                all_success = False



        if all(
            x["success"]
            for x in pages.values()
        ):

            print("===================")
            print(
                "所有 Space 启动成功"
            )

            print(
                f"耗时: {elapsed:.2f}s"
            )

            sys.exit(0)



        time.sleep(INTERVAL)



except Exception as e:

    print(
        "异常失败:",
        e
    )

    sys.exit(1)



finally:

    browser.close()
