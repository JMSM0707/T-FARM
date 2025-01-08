from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from colorama import *
from datetime import datetime
from fake_useragent import FakeUserAgent
import asyncio, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Teneo:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Origin": "https://dashboard.teneo.pro",
            "Referer": "https://dashboard.teneo.pro/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random,
            "X-Api-Key": "OwAG3kib1ivOJG4Y0OCZ8lJETa6ypvsDtGmdhcjA"
        }
        self.proxies = []
        self.proxy_index = 0

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}Teneo - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_auto_proxies(self):
        url = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url) as response:
                    response.raise_for_status()
                    content = await response.text()
                    with open('proxy.txt', 'w') as f:
                        f.write(content)

                    self.proxies = content.splitlines()
                    if not self.proxies:
                        self.log(f"{Fore.RED + Style.BRIGHT}No proxies found in the downloaded list!{Style.RESET_ALL}")
                        return
                    
                    self.log(f"{Fore.GREEN + Style.BRIGHT}Proxies successfully downloaded.{Style.RESET_ALL}")
                    self.log(f"{Fore.YELLOW + Style.BRIGHT}Loaded {len(self.proxies)} proxies.{Style.RESET_ALL}")
                    self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                    await asyncio.sleep(3)
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed to load proxies: {e}{Style.RESET_ALL}")
            return []
        
    async def load_manual_proxy(self):
        try:
            if not os.path.exists('manual_proxy.txt'):
                print(f"{Fore.RED + Style.BRIGHT}Proxy file 'manual_proxy.txt' not found!{Style.RESET_ALL}")
                return

            with open('manual_proxy.txt', "r") as f:
                proxies = f.read().splitlines()

            self.proxies = proxies
            self.log(f"{Fore.YELLOW + Style.BRIGHT}Loaded {len(self.proxies)} proxies.{Style.RESET_ALL}")
            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
            await asyncio.sleep(3)
        except Exception as e:
            print(f"{Fore.RED + Style.BRIGHT}Failed to load manual proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        
        return f"http://{proxies}" # Change with yours proxy schemes if your proxy not have schemes [http:// or socks5://]

    def get_next_proxy(self):
        if not self.proxies:
            self.log(f"{Fore.RED + Style.BRIGHT}No proxies available!{Style.RESET_ALL}")
            return None

        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.check_proxy_schemes(proxy)
    
    def load_accounts(self):
        try:
            if not os.path.exists('accounts.json'):
                self.log(f"{Fore.RED}File 'accounts.json' tidak ditemukan.{Style.RESET_ALL}")
                return

            with open('accounts.json', 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    def hide_email(self, email):
        local, domain = email.split('@', 1)
        hide_local = local[:3] + '*' * 3 + local[-3:]
        return f"{hide_local}@{domain}"
        
    async def user_login(self, email: str, password: str, proxy=None, retries=5):
        url = "https://auth.teneo.pro/api/login"
        data = json.dumps({"email":email, "password":password})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"

        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}GET ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(2)
                else:
                    return None
        
    async def connect_websocket(self, email: str, token: str, use_proxy: bool, proxy=None, retries=5):
        wss_url = f"wss://secure.ws.teneo.pro/websocket?accessToken={token}&version=v0.2"
        headers = {
            "Host": "secure.ws.teneo.pro",
            "Connection": "Upgrade",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": FakeUserAgent().random,
            "Upgrade": "websocket",
            "Origin": "chrome-extension://emcclcoaglgcpoognfiggmhnhgabppkm",
            "Sec-WebSocket-Version": "13",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Sec-WebSocket-Key": "g0PDYtLWQOmaBE5upOBXew==",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
        }
        ping_count = 0

        try:
            while True:
                connector = ProxyConnector.from_url(proxy) if proxy else None
                session = ClientSession(connector=connector, timeout=ClientTimeout(total=120))
                for attempt in range(retries):
                    try:
                        async with session:
                            async with session.ws_connect(wss_url, headers=headers) as wss:
                                while True:
                                    try:
                                        result = await wss.receive_json(timeout=120)
                                        if result and result["message"] == "Connected successfully":
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.GREEN + Style.BRIGHT} Websocket Is Connected {Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT}With Proxy {proxy}{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}] [ Earning{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} Today {result['pointsToday']} Points {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} Total {result['pointsTotal']} Points {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                            )
                                            
                                        elif result and result["message"] == "Pulse from server":
                                            ping_count += 1
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.GREEN + Style.BRIGHT} PING {ping_count} Success {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}] [ Earning{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} Today {result['pointsToday']} Points {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} Total {result['pointsTotal']} Points {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} Heartbeat {result['heartbeats']} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                            )
                                        await asyncio.sleep(3)

                                        for _ in range(90):
                                            await wss.send_json({"type":"PING"})
                                            print(
                                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                                f"{Fore.YELLOW + Style.BRIGHT}Wait For 15 Minutes For Next Ping.{Style.RESET_ALL}",
                                                end="\r",
                                                flush=True
                                            )
                                            await asyncio.sleep(10)

                                        await asyncio.sleep(3)

                                    except asyncio.TimeoutError as e:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                            f"{Fore.RED + Style.BRIGHT} Websocket Connection Timeout. {Style.RESET_ALL}"
                                            f"{Fore.YELLOW + Style.BRIGHT}Reconnecting...{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                        break

                    except Exception as e:
                        if attempt < retries - 1:
                            await asyncio.sleep(2)
                            continue
                        
                        text = 'Retrying...'
                        if use_proxy:
                            text = 'Retrying With Next Proxy...'

                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Websocket Isn't Connected. {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}{text}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                        if use_proxy:
                            proxy = self.get_next_proxy()

        except asyncio.CancelledError:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT} Websocket Connection Is Closed {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
        finally:
            await session.close()
        
    async def question(self):
        while True:
            try:
                print("1. Run With Auto Proxy")
                print("2. Run With Manual Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Auto Proxy" if choose == 1 else 
                        "With Manual Proxy" if choose == 2 else 
                        "Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Selected.{Style.RESET_ALL}")
                    await asyncio.sleep(1)
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")
        
    async def process_accounts(self, email: str, password: str, use_proxy: bool):
        hide_email = self.hide_email(email)
        proxy = None

        if use_proxy:
            proxy = self.get_next_proxy()

        login = None
        while login is None:
            login = await self.user_login(email, password, proxy)
            if not login:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {hide_email} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}With Proxy {proxy}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
                await asyncio.sleep(1)

                if not use_proxy:
                    return
            
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}Try With Next Proxy...{Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
                
                proxy = self.get_next_proxy()
                continue

            token = login['access_token']
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {hide_email} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}With Proxy {proxy}{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
            )
            await asyncio.sleep(1)

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Try Connect to Websocket...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            
            await self.connect_websocket(email, token, use_proxy, proxy)
    
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No accounts loaded from 'accounts.json'.{Style.RESET_ALL}")
                return

            use_proxy_choice = await self.question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )
            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            if use_proxy and use_proxy_choice == 1:
                await self.load_auto_proxies()
            elif use_proxy and use_proxy_choice == 2:
                await self.load_manual_proxy()
            
            while True:
                tasks = []
                for account in accounts:
                    email = account.get('Email')
                    password = account.get('Password')

                    if email and password:
                        tasks.append(self.process_accounts(email, password, use_proxy))

                await asyncio.gather(*tasks)
                await asyncio.sleep(3)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = Teneo()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Teneo - BOT{Style.RESET_ALL}                                       "                              
        )