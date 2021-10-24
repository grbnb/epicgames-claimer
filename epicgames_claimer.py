import argparse
import asyncio
import json
import os
import signal
import sys
import time
from getpass import getpass
from json.decoder import JSONDecodeError
from typing import Dict, List, Optional, Tuple, Union

import requests
import schedule
from pyppeteer import launch, launcher
from pyppeteer.element_handle import ElementHandle
from pyppeteer.network_manager import Request


__version__ = "1.5.6"


if "--enable-automation" in launcher.DEFAULT_ARGS:
    launcher.DEFAULT_ARGS.remove("--enable-automation")
# Solve the issue of zombie processes
if "SIGCHLD" in dir(signal):
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)


def log(text: str, level: str = "info") -> None:
    localtime = time.asctime(time.localtime(time.time()))
    if level == "info":
        print("[{}] {}".format(localtime, text))
    elif level == "warning":
        print("\033[33m[{}] Warning: {}\033[0m".format(localtime, text))
    elif level == "error":
        print("\033[31m[{}] Error: {}\033[0m".format(localtime, text))


class notifications:
    def __init__(self, serverchan_sendkey: str = None, bark_push_url: str = "https://api.day.app/push", bark_device_key: str = None, telegram_bot_token: str = None, telegram_chat_id: str = None) -> None:
        self.serverchan_sendkey = serverchan_sendkey
        self.bark_push_url = bark_push_url
        self.bark_device_key = bark_device_key
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        
    def push_serverchan(self, title: str, content: str = None) -> None:
        if self.serverchan_sendkey != None:
            try:
                url = "https://sctapi.ftqq.com/{}.send".format(self.serverchan_sendkey)
                data = {"title": title}
                if content != None:
                    data["desp"] = content
                requests.post(url, data=data)
            except Exception as e:
                log("Failed to push to ServerChan. {}".format(e), "error")

    def push_bark(self, title: str, content: str = None) -> None:
        if self.bark_device_key:
            try:
                response = requests.post(
                    url=self.bark_push_url,
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=json.dumps({
                        "body": content,
                        "device_key": self.bark_device_key,
                        "title": title
                    })
                )
                log(f"Bark Response HTTP Status Code: {response.status_code}")
                log(f"Bark Response HTTP Response Body: {response.content}")
            except Exception as e:
                log("Failed to push to Bark. {}".format(e), "error")

    def push_telegram(self, content: str = None) -> None:
        if self.telegram_bot_token:
            try:
                response = requests.post(
                    url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage",
                    data = {
                        "chat_id": self.telegram_chat_id,
                        "text": content
                    }
                )
                log(f"Telegram Response HTTP Status Code: {response.status_code}")
                log(f"Telegram Response HTTP Response Body: {response.content}")
            except Exception as e:
                log("Failed to push to Telegram. {}".format(e), "error")

    def notify(self, title: str, content: str = None) -> None:
        self.push_serverchan(title, content)
        self.push_bark(title, content)
        self.push_telegram(content)


class epicgames_claimer:
    def __init__(self, data_dir: Optional[str] = None, headless: bool = True, sandbox: bool = False, chromium_path: Optional[str] = None, claimer_notifications: notifications = None, timeout: int = 180000, debug: bool = False) -> None:
        self.data_dir = data_dir
        self.headless = headless
        self.sandbox = sandbox
        self.chromium_path = chromium_path
        self._loop = asyncio.get_event_loop()
        self.browser_opened = False
        self.claimer_notifications = claimer_notifications if claimer_notifications != None else notifications()
        self.timeout = timeout
        self.debug = debug
        self.page = None
        self.open_browser()
    
    def log(self, text: str, level: str = "info") -> None:
        localtime = time.asctime(time.localtime(time.time()))
        if level == "info":
            print("[{}] {}".format(localtime, text))
        elif level == "warning":
            print("\033[33m[{}] Warning: {}\033[0m".format(localtime, text))
        elif level == "error":
            print("\033[31m[{}] Error: {}\033[0m".format(localtime, text))
        elif level == "debug":
            if self.debug:
                print("[{}] Debug: {}".format(localtime, text))

    async def _headless_stealth_async(self):
        await self.page.evaluateOnNewDocument(
            "() => {"
                "Object.defineProperty(navigator, 'appVersion', {get: () => '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36',});"
                "Object.defineProperty(navigator, 'plugins', {get: () => [{'description': 'Portable Document Format', 'filename': 'internal-pdf-viewer', 'length': 1, 'name': 'Chrome PDF Plugin'}]});"
                "Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en'],});"
                "const originalQuery = window.navigator.permissions.query;"
                "window.navigator.permissions.query = (parameters) => (parameters.name === 'notifications' ? Promise.resolve({ state: Notification.permission }) : originalQuery(parameters));"
                "window.chrome = {}; window.chrome.app = {'InstallState':'a', 'RunningState':'b', 'getDetails':'c', 'getIsInstalled':'d'}; window.chrome.csi = function(){}; window.chrome.loadTimes = function(){}; window.chrome.runtime = function(){};"
                "const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto;"
                "Reflect.defineProperty(navigator.connection,'rtt', {get: () => 150, enumerable:true});"
                "const getParameter = WebGLRenderingContext.getParameter; WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'Intel Open Source Technology Center';}; if (parameter === 37446) {return 'Mesa DRI Intel(R) Ivybridge Mobile ';}; return getParameter(parameter);};"
                "['height', 'width'].forEach(property => {const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property); Object.defineProperty(HTMLImageElement.prototype, property, {...imageDescriptor, get: function() {if (this.complete && this.naturalHeight == 0) {return 16;}; return imageDescriptor.get.apply(this);},});});"
            "}"
        )
        await self.page.evaluateOnNewDocument("window.navigator.chrome = {runtime: {}, loadTimes: function() {}, csi: function() {}, app: {}};")
        await self.page.evaluateOnNewDocument("window.navigator.language = {runtime: {}, loadTimes: function() {}, csi: function() {}, app: {}};")
        await self.page.setExtraHTTPHeaders({"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"})
        await self.page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36")

    async def _open_browser_async(self) -> None:
        if not self.browser_opened:
            if "win" in launcher.current_platform():
                if self.chromium_path == None and os.path.exists("chrome-win32"):
                    self.chromium_path = "chrome-win32/chrome.exe"
            browser_args = [
                "--disable-infobars",
                "--blink-settings=imagesEnabled=false",
                "--no-first-run",
                "--disable-gpu"
            ]
            if not self.sandbox:
                browser_args.append("--no-sandbox")
            self.browser = await launch(
                options={"args": browser_args, "headless": self.headless}, 
                userDataDir=None if self.data_dir == None else os.path.abspath(self.data_dir), 
                executablePath=self.chromium_path,
            )
            self.page = (await self.browser.pages())[0]
            await self.page.setViewport({"width": 1000, "height": 600})
            # Async callback functions aren't possible to use (Refer to https://github.com/pyppeteer/pyppeteer/issues/220).
            # await self.page.setRequestInterception(True)
            # self.page.on('request', self._intercept_request_async)
            if self.headless:
                await self._headless_stealth_async()
            self.browser_opened = True
        # await self._refresh_cookies_async()

    async def _refresh_cookies_async(self) -> None:
        await self._navigate_async("https://www.epicgames.com/store/en-US/")
    
    async def _intercept_request_async(self, request: Request) -> None:
        if request.resourceType in ["image", "media", "font"]:
            await request.abort()
        else:
            await request.continue_()
        
    async def _close_browser_async(self):
        if self.browser_opened:
            await self.browser.close()
            self.browser_opened = False
    
    async def _type_async(self, selector: str, text: str, sleep: Union[int, float] = 0) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep)
        await self.page.type(selector, text)

    async def _click_async(self, selector: str, sleep: Union[int, float] = 2, timeout: int = 30000, frame_index: int = 0) -> None:
        if frame_index == 0:
            await self.page.waitForSelector(selector, options={"timeout": timeout})
            await asyncio.sleep(sleep)
            await self.page.click(selector)
        else:
            await self.page.waitForSelector("iframe:nth-child({})".format(frame_index), options={"timeout": timeout})
            frame = self.page.frames[frame_index]
            await frame.waitForSelector(selector)
            await asyncio.sleep(sleep)
            await frame.click(selector)

    async def _get_text_async(self, selector: str) -> str:
        await self.page.waitForSelector(selector)
        return await (await (await self.page.querySelector(selector)).getProperty("textContent")).jsonValue()

    async def _get_texts_async(self, selector: str) -> List[str]:
        texts = []
        try:
            await self.page.waitForSelector(selector)
            for element in await self.page.querySelectorAll(selector):
                texts.append(await (await element.getProperty("textContent")).jsonValue())
        except:
            pass
        return texts

    async def _get_element_text_async(self, element: ElementHandle) -> str:
        return await (await element.getProperty("textContent")).jsonValue()

    async def _get_property_async(self, selector: str, property: str) -> str:
        await self.page.waitForSelector(selector)
        return await self.page.evaluate("document.querySelector('{}').getAttribute('{}')".format(selector, property))

    async def _get_links_async(self, selector: str, filter_selector: str, filter_value: str) -> List[str]:
        links = []
        try:
            await self.page.waitForSelector(selector)
            elements = await self.page.querySelectorAll(selector)
            judgement_texts = await self._get_texts_async(filter_selector)
        except:
            return []
        for element, judgement_text in zip(elements, judgement_texts):
            if judgement_text == filter_value:
                link = await (await element.getProperty("href")).jsonValue()
                links.append(link)
        return links

    async def _find_async(self, selectors: Union[str, List[str]], timeout: int = None) -> Union[bool, int]:
        if type(selectors) == str:
            try:
                if timeout == None:
                    timeout = 1000
                await self.page.waitForSelector(selectors, options={"timeout": timeout})
                return True
            except:
                return False
        elif type(selectors) == list:
            if timeout == None:
                timeout = 300000
            for _ in range(int(timeout / 1000 / len(selectors))):
                for i in range(len(selectors)):
                    if await self._find_async(selectors[i], timeout=1000):
                        return i
            return -1
        else:
            raise ValueError
    
    async def _find_and_not_find_async(self, find_selector: str, not_find_selector: str, timeout: int = 60000) -> int:
        for _ in range(int(timeout / 1000 / 2)):
            if await self._find_async(find_selector, timeout=1000):
                return 0
            elif not await self._find_async(not_find_selector, timeout=1000):
                return 1
        return -1

    async def _try_click_async(self, selector: str, sleep: Union[int, float] = 2) -> bool:
        try:
            await asyncio.sleep(sleep)
            await self.page.click(selector)
            return True
        except:
            return False

    async def _get_elements_async(self, selector: str) -> Union[List[ElementHandle], None]:
        try:
            await self.page.waitForSelector(selector)
            return await self.page.querySelectorAll(selector)
        except:
            return None

    async def _wait_for_element_text_change_async(self, element: ElementHandle, text: str, timeout: int = 30) -> None:
        if await self._get_element_text_async(element) != text:
            return
        for _ in range(timeout):
            await asyncio.sleep(1)
            if await self._get_element_text_async(element) != text:
                return
        raise TimeoutError("Waiting for element \"{}\" text content change failed: timeout {}s exceeds".format(element, timeout))

    async def _navigate_async(self, url: str, timeout: int = 30000, reload: bool = True) -> None:
        if self.page.url == url and not reload:
            return
        await self.page.goto(url, options={"timeout": timeout})
    
    async def _get_json_async(self, url: str, arguments: Dict[str, str] = None) -> dict:
        response_text = await self._get_async(url, arguments)
        try:
            response_json = json.loads(response_text)
        except JSONDecodeError:
            response_text_partial = response_text if len(response_text) <= 96 else response_text[0:96]
            raise ValueError("Epic Games returnes content that cannot be resolved. Response: {} ...".format(response_text_partial))
        return response_json

    async def _login_async(self, email: str, password: str, verifacation_code: str = None, interactive: bool = True, remember_me: bool = True) -> None:
        self.log("Start to login.", level="debug")
        if email == None or email == "":
            raise ValueError("Email can't be null.")
        if password == None or password == "":
            raise ValueError("Password can't be null.")
        await self._navigate_async("https://www.epicgames.com/store/en-US/", timeout=self.timeout, reload=False)
        await self._click_async("#user", timeout=self.timeout)
        await self._click_async("#login-with-epic", timeout=self.timeout)
        await self._type_async("#email", email)
        await self._type_async("#password", password)
        if not remember_me:
            await self._click_async("#rememberMe")
        await self._click_async("#sign-in[tabindex='0']", timeout=self.timeout)
        login_result = await self._find_async(["#talon_frame_login_prod[style*=visible]", "div.MuiPaper-root[role=alert] h6[class*=subtitle1]", "input[name=code-input-0]", "#user"], timeout=self.timeout)
        if login_result == -1:
            raise TimeoutError("Chcek login result timeout.")
        elif login_result == 0:
            raise PermissionError("CAPTCHA is required for unknown reasons.")
        elif login_result == 1:
            alert_text = await self._get_text_async("div.MuiPaper-root[role=alert] h6[class*=subtitle1]")
            raise PermissionError("From Epic Games: {}".format(alert_text))
        elif login_result == 2: 
            if interactive:
                await self._type_async("input[name=code-input-0]", input("Verification code: "))
            else:
                await self._type_async("input[name=code-input-0]", verifacation_code)
            await self._click_async("#continue[tabindex='0']", timeout=self.timeout)
            verify_result = await self._find_async(["#modal-content div[role*=alert]", "#user"])
            if verify_result == -1:
                raise TimeoutError("Chcek login result timeout.")
            elif verify_result == 0:
                alert_text = await self._get_text_async("#modal-content div[role*=alert]")
                raise PermissionError("From Epic Games: {}".format(alert_text))
        self.log("Login end.", level="debug")

    async def _need_login_async(self, use_api: bool = False) -> bool:
        need_login = False
        if use_api:
            page_content_json = await self._get_json_async("https://www.epicgames.com/account/v2/ajaxCheckLogin")
            need_login = page_content_json["needLogin"]
        else:
            await self._navigate_async("https://www.epicgames.com/store/en-US/", timeout=self.timeout)
            if (await self._get_property_async("#user", "data-component")) == "SignedIn":
                need_login = False
            else:
                need_login = True
        self.log(f"Need Login: {need_login}.", level="debug")
        return need_login
    
    async def _purchase_async(self, purchase_url: str) -> Tuple[int, str]:
        await self._navigate_async(purchase_url, timeout=self.timeout)
        await self._click_async("#purchase-app button[class*=confirm]:not([disabled])", timeout=self.timeout)
        await self._try_click_async("#purchaseAppContainer div.payment-overlay button.payment-btn--primary")
        result = await self._find_and_not_find_async("#purchase-app div[class*=alert]", "#purchase-app > div", timeout=self.timeout)
        if result == 0:
            message = await self._get_text_async("#purchase-app div[class*=alert]:not([disabled])")
            return (result, message)
        elif result == 1:
            return (result, "")
        elif result == -1:
            return (result, "Timed out.")

    async def _claim_async(self) -> List[str]:
        free_games = await self._get_weekly_free_games_async()
        self.log(f"Free games: {free_games}", level="debug")
        self.log(f"Found {len(free_games)} base game(s) to be claimed.", level="debug")
        claimed_game_titles = []
        alert_text_list = []
        check_claim_result_failed = []
        for game in free_games:
            self.log(f"Claiming {game['title']} ...", level="debug")
            if not await self._is_owned_async(game["offer_id"], game["namespace"]):
                result, message = await self._purchase_async(game["purchase_url"])
                if result == 0:
                    alert_text_list.append(message)
                elif result == 1:
                    claimed_game_titles.append(game["title"])
                elif result == -1:
                    check_claim_result_failed.append(game["title"])
            else:
                self.log(f"{game['title']}: Already owned this base game.", level="debug")
            free_dlcs = await self._get_free_dlcs_async(game["namespace"])
            self.log(f"{game['title']}: Free DLC(s): {free_dlcs}", level="debug")
            self.log(f"{game['title']}: Found {len(free_dlcs)} DLC(s).", level="debug")
            for dlc in free_dlcs:
                self.log(f"{game['title']}: Claiming {dlc['title']} (offerid={dlc['offer_id']}, namespace={dlc['namespace']}) ...", level="debug")
                if not await self._is_owned_async(dlc["offer_id"], dlc["namespace"]):
                    result, message = await self._purchase_async(dlc["purchase_url"])
                    if result == 0:
                        alert_text_list.append(message)
                    elif result == 1:
                        claimed_game_titles.append(dlc["title"])
                    elif result == -1:
                        check_claim_result_failed.append(dlc["title"])
                else:
                    self.log(f"{game['title']}: Already owned {dlc['title']}.", level="debug")
            self.log(f"{game['title']}: Claim end.", level="debug")
        if len(alert_text_list) > 0:
            raise PermissionError("From Epic Games: {}".format(str(alert_text_list).strip("[]").replace("'", "").replace(",", "")))
        elif len(check_claim_result_failed) > 0:
            raise TimeoutError("Check claim result failed: {}.".format(str(check_claim_result_failed).strip("[]").replace("'", "")))
        else:
            return claimed_game_titles
    
    async def _get_authentication_method_async(self) -> Optional[str]:
        page_content_json = await self._get_json_async("https://www.epicgames.com/account/v2/security/settings/ajaxGet")
        if page_content_json["settings"]["enabled"] == False:
            return None
        else:
            return page_content_json["settings"]["defaultMethod"]
    
    def _quit(self, signum = None, frame = None) -> None:
        try:
            self.close_browser()
        except:
            pass
        exit(1)

    def _screenshot(self, path: str) -> None:
        return self._loop.run_until_complete(self.page.screenshot({"path": path}))    
        
    async def _post_json_async(self, url: str, data: str, host: str = "www.epicgames.com", sleep: Union[int, float] = 2):
        await asyncio.sleep(sleep)
        if not host in self.page.url:
            await self._navigate_async("https://{}".format(host))
        response = await self.page.evaluate("""
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "{}", true);
            xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xmlhttp.send('{}');
            xmlhttp.responseText;
        """.format(url, data))
        return response

    async def _post_async(self, url: str, data: dict, host: str = "www.epicgames.com", sleep: Union[int, float] = 2) -> str:
        await asyncio.sleep(sleep)
        if not host in self.page.url:
            await self._navigate_async("https://{}".format(host))
        evaluate_form = "var form = new FormData();\n"
        for key, value in data.items():
            evaluate_form += "form.append(`{}`, `{}`);\n".format(key, value)
        response = await self.page.evaluate(evaluate_form + """
            var form = new FormData();
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", `{}`, true);
            xmlhttp.send(form);
            xmlhttp.responseText;
        """.format(url))
        return response

    async def _get_account_id_async(self):
        if await self._need_login_async():
            return None
        else:
            await self._navigate_async("https://www.epicgames.com/account/personal")
            account_id =  (await self._get_text_async("#personalView div.paragraph-container p")).split(": ")[1]
            return account_id
    
    async def _get_async(self, url: str, arguments: Dict[str, str] = None, sleep: Union[int, float] = 2):
        args = ""
        if arguments != None:
            args = "?"
            for key, value in arguments.items():
                args += "{}={}&".format(key, value)
            args = args.rstrip("&")
        await self._navigate_async(url + args)
        response_text = await self._get_text_async("body")
        await asyncio.sleep(sleep)
        return response_text

    async def _get_game_infos_async(self, url_slug: str):
        game_infos = {}
        response= await self._get_json_async("https://store-content.ak.epicgames.com/api/zh-CN/content/products/{}".format(url_slug))
        game_infos["product_name"] = response["productName"]
        game_infos["namespace"] = response["namespace"]
        game_infos["pages"] = []
        for page in response["pages"]:
            game_info_page = {}
            if page["offer"]["hasOffer"]:
                game_info_page["offer_id"] = page["offer"]["id"]
                game_info_page["namespace"] = page["offer"]["namespace"]
                game_infos["pages"].append(game_info_page)
        return game_infos
        
    def _get_purchase_url(self, namespace:str, offer_id: str):
        purchase_url = "https://www.epicgames.com/store/purchase?lang=en-US&namespace={}&offers={}".format(namespace, offer_id)
        return purchase_url
            
    async def _get_weekly_free_games_async(self) -> List[Dict[str, str]]:
        response_text = await self._get_async("https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions")
        response_json = json.loads(response_text)
        free_game_infos = []
        for item in response_json["data"]["Catalog"]["searchStore"]["elements"]:
            free_game_info = {}
            if {"path": "freegames"} in item["categories"]:
                if item["price"]["totalPrice"]["discountPrice"] == 0 and item["price"]["totalPrice"]["originalPrice"] != 0:
                    if item["offerType"] == "BASE_GAME":
                        free_game_info["title"] = item["title"]
                        free_game_info["url_slug"] = item["urlSlug"]
                        free_game_info["namespace"] = item["namespace"]
                        free_game_info["offer_id"] = item["id"]
                        free_game_info["url"] = "https://www.epicgames.com/store/p/" + free_game_info["url_slug"]
                        free_game_info["purchase_url"] = "https://www.epicgames.com/store/purchase?lang=en-US&namespace={}&offers={}".format(free_game_info["namespace"], free_game_info["offer_id"])
                        free_game_infos.append(free_game_info)
        return free_game_infos
    
    async def _get_free_dlcs_async(self, namespace: str) -> List[Dict[str, str]]:
        args = {
            "query": "query searchStoreQuery($namespace: String, $category: String, $freeGame: Boolean, $count: Int){Catalog{searchStore(namespace: $namespace, category: $category, freeGame: $freeGame, count: $count){elements{title id namespace}}}}",
            "variables": '{{"namespace": "{}", "category": "digitalextras/book|addons|digitalextras/soundtrack|digitalextras/video", "freeGame": true, "count": 1000}}'.format(namespace)
        }
        response = await self._get_json_async("https://www.epicgames.com/graphql", args)
        free_items = []
        for item in response["data"]["Catalog"]["searchStore"]["elements"]:
            free_item = {}
            free_item["title"] = item["title"]
            free_item["offer_id"] = item["id"]
            free_item["namespace"] = item["namespace"]
            free_item["purchase_url"] = self._get_purchase_url(item["namespace"], item["id"])
            free_items.append(free_item)
        return free_items
    
    async def _screenshot_async(self, path: str) -> None:
        await self.page.screenshot({"path": path})
    
    def add_quit_signal(self):
        signal.signal(signal.SIGINT, self._quit)
        signal.signal(signal.SIGTERM, self._quit)
        if "SIGBREAK" in dir(signal):
            signal.signal(signal.SIGBREAK, self._quit)
        if "SIGHUP" in dir(signal):
            signal.signal(signal.SIGHUP, self._quit)

    async def _is_owned_async(self, offer_id: str, namespace: str) -> bool:
        args = {
            "query": "query launcherQuery($namespace: String!, $offerId: String!){Launcher{entitledOfferItems(namespace: $namespace, offerId: $offerId){entitledToAnyItemInOffer}}}",
            "variables": "{{\"namespace\": \"{}\", \"offerId\": \"{}\"}}".format(namespace, offer_id)
        }
        response = await self._get_json_async("https://www.epicgames.com/graphql", args)
        try:
            owned = response["data"]["Launcher"]["entitledOfferItems"]["entitledToAnyItemInOffer"]
        except:
            raise ValueError("The returned data seems to be incorrect.")
        return owned

    async def _try_get_webpage_content_async(self) -> Optional[str]:
        try:
            if self.browser_opened:
                webpage_content = await self._get_text_async('body')
                return webpage_content
        except:
            pass
    
    async def _run_once_async(self, interactive: bool = True, email: str = None, password: str = None, verification_code: str = None, retries: int = 3, raise_error: bool = False) -> None:
        for i in range(retries):
            try:
                if not self.browser_opened:
                    await self._open_browser_async()
                break
            except Exception as e:
                if i < retries - 1:
                    self.log("{}".format(e), level="warning")
                else:
                    self.log(f"Failed to open the browser. {e}", "error")
                    self.claimer_notifications.notify("EpicGames Claimer: 错误！", f"无法打开浏览器。 {e}")
                    if raise_error:
                        await self._close_browser_async()
                        raise e
                    return
        for i in range(retries):
            try:
                if await self._need_login_async():
                    if interactive:
                        self.log("Need login.")
                        self.claimer_notifications.notify("EpicGames Claimer: 需要登录", "登录失效，需要重新登录。")
                        await self._close_browser_async()
                        email = input("Email: ")
                        password = getpass("Password: ")
                        await self._open_browser_async()
                        await self._login_async(email, password)
                        self.log("Login successed.")
                    else:
                        await self._login_async(email, password, verification_code, interactive=False)
                break
            except Exception as e:
                if i < retries - 1:
                    self.log("{}".format(e), level="warning")
                else:
                    self.log(f"Failed to login. {e}", "error")
                    self.claimer_notifications.notify("EpicGames Claimer: 错误！", f"登录失败。{e}")
                    if self.debug:
                        self.log(f"Current url: {self.page.url}", "debug")
                        webpage_content = await self._try_get_webpage_content_async()
                        self.log(f"Current webpage content: {webpage_content}", "debug")
                    await self._screenshot_async("screenshot.png")
                    if interactive:
                        await self._close_browser_async()
                        exit(1)
                    await self._close_browser_async()
                    if raise_error:
                        await self._close_browser_async()                        
                        raise e
                    return
        for i in range(retries):
            try:
                claimed_game_titles = await self._claim_async()
                if len(claimed_game_titles) > 0:
                    text = "{} has been claimed.".format(str(claimed_game_titles).strip("[]").replace("'", ""))
                    text_zh = "{} 已被成功领取。".format(str(claimed_game_titles).strip("[]").replace("'", ""))
                    self.log(text)
                    self.claimer_notifications.notify("EpicGames Claimer: Claim Successed", text_zh)
                else:
                    self.log("All available weekly free games are already in your library.")
                break
            except Exception as e:
                if i < retries - 1:
                    self.log("{}".format(e), level="warning")
                else:
                    self.log(f"Failed to claim free games. {e}", level="error")
                    self.claimer_notifications.notify("EpicGames Claimer: 错误！", f"领取失败。{e}")
                    if self.debug:
                        self.log(f"Current url: {self.page.url}", "debug")
                        webpage_content = await self._try_get_webpage_content_async()
                        self.log(f"Current webpage content: {webpage_content}", "debug")
                    await self._screenshot_async("screenshot.png")
                    await self._close_browser_async()
                    if raise_error:
                        await self._close_browser_async()
                        raise e
                    return
        await self._close_browser_async()
    
    def open_browser(self) -> None:
        return self._loop.run_until_complete(self._open_browser_async())

    def close_browser(self) -> None:
        return self._loop.run_until_complete(self._close_browser_async())
    
    def need_login(self) -> bool:
        return self._loop.run_until_complete(self._need_login_async())
    
    def login(self, email: str, password: str, verifacation_code: str = None, interactive: bool = True, remember_me: bool = True) -> None:
        return self._loop.run_until_complete(self._login_async(email, password, verifacation_code, interactive, remember_me))
        
    def claim(self) -> List[str]:
        return self._loop.run_until_complete(self._claim_async())
    
    def get_weekly_free_games(self) -> List[Dict[str, str]]:
        return self._loop.run_until_complete(self._get_weekly_free_games_async())
    
    def run_once(self, interactive: bool = True, email: str = None, password: str = None, verification_code: str = None, retries: int = 3, raise_error: bool = False) -> None:
        return self._loop.run_until_complete(self._run_once_async(interactive, email, password, verification_code, retries, raise_error))
    
    def scheduled_run(self, at: str, interactive: bool = True, email: str = None, password: str = None, verification_code: str = None, retries: int = 3) -> None:
        self.add_quit_signal()
        schedule.every().day.at(at).do(self.run_once, interactive, email, password, verification_code, retries)
        while True:
            schedule.run_pending()
            time.sleep(1)
    

def get_args(include_auto_update: bool = False) -> argparse.Namespace:
    def update_args_from_env(args: argparse.Namespace) -> argparse.Namespace:
        for key in args.__dict__.keys():
            env = os.environ.get(key.upper())
            if env != None:
                if type(args.__dict__[key]) == int:
                    args.__setattr__(key, int(env))
                elif type(args.__dict__[key]) == bool:
                    if env == "true":
                        args.__setattr__(key, True)
                    elif env == "false":
                        args.__setattr__(key, False)
                else:
                    args.__setattr__(key, env)
        return args
    parser = argparse.ArgumentParser(description="Claim weekly free games from Epic Games Store.")
    parser.add_argument("-n", "--no-headless", action="store_true", help="run the browser with GUI")
    parser.add_argument("-c", "--chromium-path", type=str, help="set path to browser executable")
    parser.add_argument("-r", "--run-at", type=str, help="set daily check and claim time, format to HH:MM, default to the current time")
    parser.add_argument("-o", "--once", action="store_true", help="claim once then exit")
    if include_auto_update:
        parser.add_argument("-a", "--auto-update", action="store_true", help="enable auto update")
    parser.add_argument("-u", "--email", "--username", type=str, help="set username/email")
    parser.add_argument("-p", "--password", type=str, help="set password")
    parser.add_argument("-t", "--verification-code", type=str, help="set verification code (2FA)")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug mode")
    parser.add_argument("-dt", "--debug-timeout", type=int, default=180000, help="set timeout in milliseconds")
    parser.add_argument("-dr", "--debug-retries", type=int, default=3, help="set the number of retries")
    parser.add_argument("-ps", "--push-serverchan-sendkey", type=str, help="set ServerChan sendkey")
    parser.add_argument("-pbu", "--push-bark-url", type=str, default="https://api.day.app/push", help="set Bark server address")
    parser.add_argument("-pbk", "--push-bark-device-key", type=str, help="set Bark device key")
    parser.add_argument("-ptt", "--push-telegram-bot-token", type=str, help="set Telegram bot token")
    parser.add_argument("-pti", "--push-telegram-chat-id", type=str, help="set Telegram chat ID")
    args = parser.parse_args()
    args = update_args_from_env(args)
    if args.run_at == None:
        localtime = time.localtime()
        args.run_at = "{0:02d}:{1:02d}".format(localtime.tm_hour, localtime.tm_min)
    if args.email != None and args.password == None:
        raise ValueError("Must input both username and password.")
    if args.email == None and args.password != None:
        raise ValueError("Must input both username and password.")
    args.interactive = True if args.email == None else False
    args.data_dir = "User_Data/Default" if args.interactive else "User_Data/{}".format(args.email)
    return args


def main(args: argparse.Namespace = None, raise_error: bool = False) -> None:
    if args == None:    
        args = get_args()
    claimer_notifications = notifications(serverchan_sendkey=args.push_serverchan_sendkey, bark_push_url=args.push_bark_url, bark_device_key=args.push_bark_device_key, telegram_bot_token=args.push_telegram_bot_token, telegram_chat_id=args.push_telegram_chat_id)
    claimer = epicgames_claimer(args.data_dir, headless=not args.no_headless, chromium_path=args.chromium_path, claimer_notifications=claimer_notifications, timeout=args.debug_timeout, debug=args.debug)
    if args.once:
        claimer.run_once(args.interactive, args.email, args.password, args.verification_code, retries=args.debug_retries, raise_error=raise_error)
    else:
        claimer.run_once(args.interactive, args.email, args.password, args.verification_code, retries=args.debug_retries)
        claimer.scheduled_run(args.run_at, args.interactive, args.email, args.password, args.verification_code)


# This is for Tencent Serverless
def main_handler(event: Dict[str, str], context: Dict[str, str]) -> None:
    cwd = os.getcwd()
    sys.path.append(cwd)
    os.chdir("/tmp")
    args = get_args()
    args.chromium_path = cwd + "/chrome-linux/chrome"
    args.once = True
    main(args, raise_error=True)


if __name__ == "__main__":
    main()
