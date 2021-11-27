import asyncio
from pyppeteer import launch, launcher
import json


URL_EPICGAMES = "https://epicgames.com/store"


if "--enable-automation" in launcher.DEFAULT_ARGS:
    launcher.DEFAULT_ARGS.remove("--enable-automation")


async def save_cookies(path) -> None:
    browser = await launch(options={"headless": False, "args": ["--disable-infobars", "--no-first-run"]})
    page = (await browser.pages())[0]
    await page.goto(URL_EPICGAMES, options={"waitUntil": []})
    input("登录成功后按Enter键: ")
    with open(path, "w") as cookies_file:
        await page.cookies()
        cookies = await page.cookies()
        cookies_file.write(json.dumps(cookies, separators=(",", ": "), indent=4))
    print(f"cookies已保存至{path}。")
    await browser.close()


if __name__ == "__main__":
    asyncio.run(save_cookies("cookies.json"))
