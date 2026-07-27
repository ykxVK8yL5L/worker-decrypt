from cloakbrowser import launch
import argparse

parser = argparse.ArgumentParser(description='Parse input data')
parser.add_argument("--url", help="Url to Browse", default="")
args = parser.parse_args()

if args.url:
    browser = launch()
    page = browser.new_page()
    page.goto(args.url)
    print(f"open url :{args.url}")

    browser.close()



 



