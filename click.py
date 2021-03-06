#!/usr/bin/python

import collections
import concurrent.futures
import logging
import logging.handlers
import os
import requests
import random
import time
import urllib
from threading import Thread

LOG_FILE = 'click.log'


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
                # self.proxy["http"] = "http://" + res
                time.sleep(0.5)
            except Exception as e:
                print(e)
                time.sleep(1)

    def getProxy(self):
        return self.proxy


class ProxyHandler1:

    def __init__(self):
        print("create proxy")
        self.apiUrl = "http://dev.kuaidaili.com/api/getproxy/?orderid=919618932650660&num=300&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=1&an_an=1&an_ha=1&sp1=1&sp2=1&quality=1&sep=4"
        self.proxy_list = []

        prefetch_thread = Thread(target=self.__fetch)
        prefetch_thread.start()

    def __fetch(self):
        while (1):
            url = self.apiUrl
            res = requests.get(url,
                               allow_redirects=True,
                               timeout=10)
            web_data = res.text
            self.__get_proxies(web_data)
            time.sleep(1000 * 10)

    def __get_proxies(self, web_data):
        pl = web_data.split('|')
        for p in pl:
            self.proxy_list.append(p)

        print(self.proxy_list)

        print("proxy num: ", len(self.proxy_list))

    def getProxy(self):
        proxy_map = {"https": "", "http": ""}
        try:
            if (len(self.proxy_list) > 0):
                n = random.randint(0, len(self.proxy_list) - 1)
                proxy_map["https"] = "http://" + self.proxy_list[n]
                proxy_map["http"] = "http://" + self.proxy_list[n]
        except Exception as e:
            print(e)
        return proxy_map


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
        self.already_run_list = []
        self.logger = logging.getLogger("ClickLogging")
        self.__setup_log()

    def __setup_log(self):
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)  # 实例化handler
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def request(self, holder, proxy_handler, url):
        try:
            self.counter += 1
            headers = {}
            headers['User-Agent'] = holder.getUA()
            # headers['Connection'] = 'close'

            proxy = proxy_handler.getProxy()

            print("proxy:", proxy)
            while proxy["https"] == "":
                # print("empty http proxy")
                time.sleep(0.5)

            # proxy['https'] = 'http://171.38.179.28:8123'
            # proxy['http'] = 'http://171.38.179.28:8123'
            # print("proxy:", proxy)
            # print("cur counter: ", self.counter)
            self.logger.info("cur counter: %d" % self.counter)
            requests.get(url,
                         proxies=proxy,
                         headers=headers,
                         allow_redirects=True,
                         timeout=10)
        except Exception as e:
            print(e)

    def run(self):
        holder = Holder()
        proxy_handler = ProxyHandler1()
        max_tasks = 200

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_tasks) as executor:
            for fi in holder.getFileList():
                # self.logger.info(fi)
                if (fi in self.already_run_list):
                    continue
                self.already_run_list.append(fi)
                with open(fi, 'rt') as f:
                    for line in f:
                        self.logger.info("cur idfa: %s" % line)
                        for addr in holder.getAddr():
                            time.sleep(0.15)
                            executor.submit(self.request, holder,
                                            proxy_handler,
                                            addr + "&idfa=" + line)
        self.logger.info("Finish total: %d" % self.counter)

if __name__ == '__main__':
    worker = Worker()
    while True:
        worker.run()
        time.sleep(3)
