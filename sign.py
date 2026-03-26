from cloakbrowser import launch

browser = launch(headless=False)
page = browser.new_page()
page.goto("https://www.iios.fun")
print(page.content())
browser.close()
