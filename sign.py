from cloakbrowser import launch

browser = launch()
page = browser.new_page()
page.goto("https://iios.fun")
print(page.content())
browser.close()
