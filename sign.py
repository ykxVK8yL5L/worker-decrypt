import asyncio
from cloakbrowser import launch_async

async def main():
    print("start...")
    browser = await launch_async()
    page = await browser.new_page()
    await page.goto("https://www.ioos.fun")
    print(await page.title())
    await browser.close()

asyncio.run(main())
