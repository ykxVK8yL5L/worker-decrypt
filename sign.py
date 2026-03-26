from cloakbrowser import launch
import argparse

parser = argparse.ArgumentParser(description='Parse user data')
parser.add_argument("--email", help="Login Email", default="")
parser.add_argument("--password", help="Login Password", default="")
args = parser.parse_args()


browser = launch()
page = browser.new_page()
page.goto("https://iios.fun")
print(page.content())
browser.close()
