
import asyncio
import collections
import concurrent.futures
import os
import requests
import random
import time
import urllib
from threading import Thread


class ProxyHandler:

    def __init__(self):
        self.proxy = {"https": ""}
        self.order = "70d8ff78674398a42e90a879683582fd"
        self.apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + self.order

        prefetch_thread = Thread(target=self.__fetch)
        prefetch_thread.start()

    def __fetch(self):
        while 1:
            try:
                res = urllib.request.urlopen(
                    self.apiUrl).read().decode().strip("\n")
                if res == "too many request":
                    time.sleep(0.5)
                    continue

                self.proxy["https"] = res
                time.sleep(0.5)
            except Exception as e:
                print(e)
                time.sleep(1)

    def getProxy(self):
        return self.proxy


class Holder:

    def __init__(self):
        self.addrList = collections.deque()
        self.fileList = collections.deque()
        self.__init()

    def __init(self):
        # ofo
        # self.addrList.append("https://lnk0.com/Mt8Edc?transaction_id=fb31665d0-832e-a698-d42c965aaf3f572602333e4cc8b0e52d9f0161f6b12000b&affiliate_id=104991&aff_sub8=")
        self.addrList.append(
            "https://global.ymtracking.com/trace?offer_id=5107479&aff_id=104991")
        # elema
        # self.addrList.append("http://network.adsmarket.com/click/j2dxlV-hqZqMY26bYMp6w4iQbJZeoYOVjWqYnGShfZuNkGqdYaGAmLdibZhmoYOU?dp=475b7bf70-7fd2-4e79-3826d7ee04223371bc19319918dee38075c1ba5fcbd000e&dp2=104991&dp3=")
        self.addrList.append(
            "https://global.ymtracking.com/trace?offer_id=5065577&aff_id=104991")
        self.travelLogs()
        self.ua_str = ["Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
                       "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25",
                       "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
                       "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11A465 Twitter for iPhone"]

    def getFileList(self):
        return self.fileList

    def getAddr(self):
        return self.addrList

    def getUA(self):
        return self.ua_str[random.randint(0, 3)]

    def travelLogs(self):
        cur_path = os.path.abspath(os.curdir)
        cur_path += "/logs/"
        for path, d, files in os.walk(cur_path):
            for filename in files:
                self.fileList.append(os.path.join(path, filename))


class Worker:

    def __init__(self):
        self.counter = 0

    def request(self, holder, proxy_handler, url):
        print("request....")
        self.counter += 1
        headers = {}
        headers['User-Agent'] = holder.getUA()

        proxy = proxy_handler.getProxy()

        while proxy["https"] == "":
            print("proxy empty")
            time.sleep(0.5)

        try:
            print("url: ", url)
            print("proxy: ", proxy)
            requests.get(url,
                         proxies=proxy,
                         headers=headers,
                         allow_redirects=True,
                         timeout=2)
            print("total counter: ", self.counter)
        except Exception as e:
            print(e)

    def run(self):
        holder = Holder()
        proxy_handler = ProxyHandler()
        max_tasks = 1000
        # index = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_tasks) as executor:
            for fi in holder.getFileList():
                with open(fi, 'rt') as f:
                    for line in f:
                        for addr in holder.getAddr():
                            time.sleep(0.2)
                            executor.submit(self.request, holder,
                                            proxy_handler,
                                            addr + "&idfa=" + line)

if __name__ == '__main__':
    worker = Worker()
    worker.run()
    print("Finish.......................")

# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
# 	for i in range(0, 9):
# 		executor.submit(dosth, i)
