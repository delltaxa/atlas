#!/usr/bin/python

import datetime
from colorama import Fore

version = "1.0.2-A"
site = "https://atlas.tool/"
text = f"""{Fore.BLUE}
    _     
   /|\      _____ _____ __    _____ _____ 
  / | \    |  _  |_   _|  |  |  _  |   __| {Fore.MAGENTA}Version {Fore.YELLOW}{version}{Fore.BLUE}
 / /\__\   |     | | | |  |__|     |__   | {Fore.WHITE}{site}{Fore.BLUE}
/_/__|__\  |__|__| |_| |_____|__|__|_____| {Fore.WHITE}The {Fore.BLUE}Async{Fore.WHITE} Version

{Fore.WHITE}"""

def line(len, ch):
    return ch*len

import asyncio

import json
import socket
import requests
import urllib
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
class atlas:
    miss_configured = []

    dev_ports = [
        8080, 8081, 4434,
	    5000, 3000, 3001,
	    4000, 4443, 5000,
	    5001, 8443
    ]

    def load_miss_configured():
        f = open('busting.txt')
        data = json.load(f)
        f.close()
        atlas.miss_configured = data

    def port_open(addr, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((addr, port))
        
        if result == 0:
            sock.close()
            return True
        else:
            sock.close()
            return False

    def base_url(url):
        https = False
        if url.strip().lower().startswith("https://"):
            https = True
        
        domain = atlas.get_domain(url=url)

        ht_str = "http"
        if https:
            ht_str += "s"
        ht_str += "://"

        return ht_str + domain

    def dev_links(url):
        results = []
        host = atlas.get_domain(url=url)
        addr = atlas.host2ip(host=host)
        for port in atlas.dev_ports:
            open = atlas.port_open(addr, port)
            if open:
                results.append(atlas.base_url(url) + ":" + str(port) + "/")

        return results

    def is_gruzifix(url):
        try:
            f = urlopen(urljoin(url, "/gruzifix.atlas"))
            content = requests.get(urljoin(url, "/gruzifix.atlas"), allow_redirects=False).content
            content = content.decode("utf-8")
            return True
        except urllib.error.HTTPError:
            return False

    miss_conf_results = []
    async def handle_miss(url, should_len, gruzifix, x):
        critlevel = []
        paths     = []
        rootpaths = []

        try: critlevel = x["critLevel"]
        except: pass

        try: paths = x["paths"]
        except: pass

        try: rootpaths = x["rootPaths"]
        except: pass

        critcolor = Fore.RED
        
        if critlevel == "1":
            critcolor = Fore.GREEN
        elif critlevel == "2":
            critcolor = Fore.YELLOW

        allpaths = paths+rootpaths
        
        for path in allpaths:
            try:
                f = urlopen(urljoin(url, path))
                
                fg_color = Fore.GREEN
            
                if gruzifix == True:
                    fg_color = Fore.YELLOW

                if f.code == 200 and gruzifix:
                    continue

                if f.code != 404:
                    atlas.miss_conf_results.append(path + " " + line(should_len - path.__len__() - 1 - "[00:00:00] [INFO]  ".__len__() - (str(f.code).__len__() + 2), " ") + critcolor + f"{critlevel} " + fg_color + str(f.code) + Fore.WHITE)
            except urllib.error.HTTPError:
                pass
        
        return "atlas"

    async def get_miss_configured(url, should_len):
        results = []

        gruzifix = atlas.is_gruzifix(url)

        f = await asyncio.gather(*[atlas.handle_miss(url, should_len, gruzifix, x) for x in atlas.miss_configured])

        results = atlas.miss_conf_results

        return results

    def get_robots(url):
        allows = []
        disallows = []

        robots_txt = (requests.get(urljoin(atlas.base_url(url=url), "robots.txt")).content).decode("utf-8")

        robots_lines_split = robots_txt.split("\n")

        current_agent = ""
        for line in robots_lines_split:
            if line.strip().lower().startswith("user-agent"):
                if line.strip().lower() == "user-agent: *":
                    current_agent = "*"
                else:
                    current_agent = "."
            else:
                if current_agent == "*":
                    if line.strip().lower().startswith("disallow:"):
                        item = line.strip()[9:line.strip().__len__()].strip()

                        if item.strip() != "":
                            disallows.append(item)

                    if line.strip().lower().startswith("allow:"):
                        item = line.strip()[6:line.strip().__len__()].strip()

                        if item.strip() != "":
                            allows.append(item)
        
        return {"allow": allows, "disallow": disallows}

    def get_domain(url):
        return urlparse(url).netloc
    
    def host2ip(host):
        return socket.gethostbyname(host)

    def get_server(url):
        response = requests.head(url).headers

        try:
            return response["server"]
        except KeyError:
            return "unkown"

def ctime():
    return datetime.datetime.today().strftime('%H:%M:%S')

async def makescan(url):
    atlas.load_miss_configured()

    liner = line((f"[00:00:00] [EVENT] Getting info about ({url})").__len__(), '-')

    longestUrl = 0

    for x in atlas.miss_configured:
        paths = []
        rootpaths = []
        
        try: paths = x["paths"]
        except: pass
        
        try: rootpaths = x["rootPaths"]
        except: pass

        allpaths = paths+rootpaths
        
        for path in allpaths:
            if path.__len__()  > longestUrl:
                longestUrl = path.__len__()

    while liner.__len__() < longestUrl+25:
        liner += '-'

    print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.BLUE}EVENT{Fore.WHITE}] Getting info about ({Fore.BLUE}{url}{Fore.WHITE})")

    print(liner)

    print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}]  DOMAIN.: {atlas.get_domain(url)}")
    print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}]  SERVER.: {atlas.get_server(url)}")
    print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}]  ADDRESS: {atlas.host2ip(atlas.get_domain(url))}")
   
    print(liner)
    print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.BLUE}EVENT{Fore.WHITE}] Checking for miss-configured files")
    print(liner)

    misscfg = await atlas.get_miss_configured(url, liner.__len__())
    for file in misscfg:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}]  {file}")
    if misscfg.__len__() == 0:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}] {Fore.RED} No miss-configuration found!{Fore.WHITE}")

    print(liner)

    print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.BLUE}EVENT{Fore.WHITE}] Scanning for dev-ports")    

    print(liner)

    devports = atlas.dev_links(url)
    for file in devports:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}]  {file}")
    
    if devports.__len__() == 0:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}] {Fore.RED} No dev-ports found!{Fore.WHITE}")

    print(liner)

    print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.BLUE}EVENT{Fore.WHITE}] Scanning ({Fore.BLUE}robots.txt{Fore.WHITE})")    

    print(liner)

    robots = atlas.get_robots(url)
    allows = robots['allow']
    disallows = robots['disallow']

    for allow in allows:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}]  {Fore.GREEN}ALLOW    {Fore.WHITE}{allow}")

    for disallow in disallows:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}]  {Fore.RED}DISALLOW {Fore.WHITE}{disallow}")

    if allows.__len__() == 0 and disallows.__len__() == 0:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.GREEN}INFO{Fore.WHITE}] {Fore.RED} No interessting items found!{Fore.WHITE}")


import sys
async def main():
    print(text)

    if sys.argv.__len__() < 2:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.RED}ERROR{Fore.WHITE}] {Fore.WHITE} No url specified")
        exit()

    await makescan(sys.argv[1])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.RED}ERROR{Fore.WHITE}] {Fore.WHITE} KeyboardInterrupt")
    except requests.exceptions.ConnectionError:
        print(f"[{Fore.CYAN}{ctime()}{Fore.WHITE}] [{Fore.RED}ERROR{Fore.WHITE}] {Fore.WHITE} HostNotFound")
    exit()
