
# import asyncio
import collections
# import concurrent.futures
import logging
import logging.handlers
import os
import requests
import random
import time
import urllib
import ssl
from threading import Thread
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor

LOG_FILENAME = 'run_log'


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

                self.proxy["https"] = "https://" + res
                self.proxy["http"] = "http://" + res
                time.sleep(0.5)
            except Exception as e:
                # print(e)
                time.sleep(1)

    def getProxy(self):
        return self.proxy


class Holder:

    def __init__(self):
        self.addrList = collections.deque()
        self.fileList = collections.deque()
        self.__init()

    def __init(self):
        self.addrList.append(
            "https://global.ymtracking.com/trace?offer_id=5107479&aff_id=104991")
        self.addrList.append(
            "https://global.ymtracking.com/trace?offer_id=5065577&aff_id=104991")
        self.addrList.append(
            "http://svr.dotinapp.com/ics?sid=1217&adid=4006512")
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
        cur_path += "/ioslogs/"
        for path, d, files in os.walk(cur_path):
            for filename in files:
                self.fileList.append(os.path.join(path, filename))


class Worker:

    def __init__(self):
        self.counter = 0
        self.click_logger = logging.getLogger("ClickLogger")
        self.__log_setup()
        self.session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))
        self.holder = Holder()
        self.proxy_handler = ProxyHandler()

    def __log_setup(self):
        self.click_logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=5)
        bf = logging.Formatter('{asctime} {name} {levelname:8s} {message}',
                               style='{')
        handler.setFormatter(bf)
        self.click_logger.addHandler(handler)

    def __do_redirect(self, sess, resp):
        print("resp:  ", resp.url)
        sess.close()
        sess = NULL
        headers = {}
        headers['User-Agent'] = self.holder.getUA()
        proxy = self.proxy_handler.getProxy()
        try:
            self.session.get(
                resp.url,
                background_callback=self.__do_redirect,
                headers=headers,
                proxies=proxy,
                allow_redirects=False,
                timeout=10)
            resp = NULL
        except Exception as e:
            resp = NULL
            print("redirect error:", e, resp.url)

    def run(self):
        max_tasks = 16
        futures = []

        proxy = self.proxy_handler.getProxy()
        while proxy["https"] == "":
            print("proxy empty")
            time.sleep(0.5)

        for fi in self.holder.getFileList():
            with open(fi, 'rt') as f:
                for line in f:
                    for addr in self.holder.getAddr():
                        headers = {}
                        headers['User-Agent'] = self.holder.getUA()
                        time.sleep(0.15)
                        self.counter += 1
                        print("cur counter: ", self.counter)
                        try:
                            # self.session.mount('https://',
                            #   SSLAdapter(ssl.PROTOCOL_TLSv1_1|PROTOCOL_TLSv1_2|ssl.PROTOCOL_SSLv3))
                            future = self.session.get(
                                addr + "&idfa=" + line, background_callback=self.__do_redirect,
                                headers=headers,
                                proxies=proxy,
                                allow_redirects=True,
                                timeout=10)
                            futures.append(future)
                            # futures[:] = []
                            if (len(futures) == 10):
                                for f in futures:
                                    print("waitttttttttttttttttt")
                                    f.result()
                                print("cleannnnnnnnnnnnnnnnnnnn")
                                futures[:] = []
                            print("futures.size: ", len(futures))
                            # future_.result()
                        except Exception as e:
                            print("request error:", e)
        # self.click_logger.info("Finish total: %d" % self.counter)

if __name__ == '__main__':
    worker = Worker()
    worker.run()
