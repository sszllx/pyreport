
import asyncio
import collections
import requests
import random
import time
import urllib
from threading import Thread


class ProxyHandler:

    def __init__(self, is_prefetch):
        self.proxy = {"https": ""}
        self.proxy_list = []
        self.order = "70d8ff78674398a42e90a879683582fd"
        self.apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + self.order
        if is_prefetch:
            self.fetching = True
            self.preFetch()

    def getProxy(self):
        return self.proxy_list

    def isFetching(self):
        return self.fetching

    def preFetch(self):
        # _thread.start_new_thread(self.__preFetch, ())
        if (len(self.proxy_list) > 0):
            self.proxy_list.clear()

        prefetch_thread = Thread(target=self.__preFetch)
        prefetch_thread.start()

    def __preFetch(self):
        while 1:
            try:
                self.fetching = True
                res = urllib.request.urlopen(
                    self.apiUrl).read().decode().strip("\n")
                print("proxy:", res)
                self.proxy_list.append(res)
                time.sleep(2)
                if (len(self.proxy_list) >= 10):
                    self.fetching = False
                    break
            except Exception as e:
                print(e)

    def preFetchOnce(self):
        while 1:
            try:
                res = urllib.request.urlopen(
                    self.apiUrl).read().decode().strip("\n")
                print("proxy:", res)
                if res == "too many request":
                    time.sleep(0.5)
                    continue

                return res
            except Exception as e:
                print(e)
                time.sleep(1)


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
        self.fileList.append("1.mobile.id")
        # self.fileList.append("3.mobile.id")
        # self.fileList.append("7.mobile.id")
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


class Worker:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        self.proxy_list = []

    @asyncio.coroutine
    def __fetch(self, holder, proxy_handler, url, is_prefetch):
        headers = {}
        headers['User-Agent'] = holder.getUA()

        proxies = {"https": ""}
        if is_prefetch:
            proxies["https"] = self.proxy_list[random.randint(0, len(self.proxy_list) - 1)]
        else:
            proxies["https"] = proxy_handler.preFetchOnce()

        print("proxies::::", proxies)

        try:
            requests.get(url,
                         proxies=proxies,
                         headers=headers,
                         allow_redirects=True,
                         timeout=10)
        except Exception as e:
            print(e)
        # print(res)

    def run(self):
        is_prefetch = False
        holder = Holder()
        proxy_handler = ProxyHandler(is_prefetch)
        counter = 0

        for fi in holder.getFileList():
            with open(fi, 'rt') as f:
                for line in f:
                    for addr in holder.getAddr():

                        if is_prefetch:
                            # waiting for prefetch proxies
                            while proxy_handler.isFetching():
                                time.sleep(1)

                        try:
                            # asyncio.ensure_future(self.__for_test())
                            self.proxy_list = proxy_handler.getProxy().copy()
                            task = asyncio.ensure_future(
                                self.__fetch(holder, proxy_handler, addr + "&idfa=" + line, is_prefetch))
                            self.tasks.append(task)
                            if (len(self.tasks) == 100):
                                print("counter: ", counter)
                                counter += 1
                                # restart prefetch thread
                                proxy_handler.preFetch()
                                self.loop.run_until_complete(
                                    asyncio.wait(self.tasks))
                                self.tasks.clear()
                                time.sleep(0.5)

                        except Exception as e:
                            print(e)

if __name__ == '__main__':
    worker = Worker()
    worker.run()
    # TODO: treat remaining tasks
