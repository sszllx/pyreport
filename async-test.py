
import aiohttp
import asyncio
import collections
import requests
import random
import time
import urllib

class ProxyHandler:
	def __init__(self):
		self.proxy = {"https": ""}
		self.__fetchProxy()

	def getProxy(self):
		return self.proxy

	def __fetchProxy(self):
		order = "70d8ff78674398a42e90a879683582fd"
		apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
		while 1:
			try:
				res = urllib.request.urlopen(apiUrl).read().decode().strip("\n")
				print("ips:" + res)
				self.proxy["https"] = res
				time.sleep(2)
			except Exception as e:
				print(e)

class Holder:
	def __init__(self):
		self.addrList = collections.deque()
		self.fileList = collections.deque()
		self.__init()

	def __init(self):
		# ofo
		# self.addrList.append("https://lnk0.com/Mt8Edc?transaction_id=fb31665d0-832e-a698-d42c965aaf3f572602333e4cc8b0e52d9f0161f6b12000b&affiliate_id=104991&aff_sub8=")
		self.addrList.append("https://global.ymtracking.com/trace?offer_id=5107479&aff_id=104991")
		# elema
		# self.addrList.append("http://network.adsmarket.com/click/j2dxlV-hqZqMY26bYMp6w4iQbJZeoYOVjWqYnGShfZuNkGqdYaGAmLdibZhmoYOU?dp=475b7bf70-7fd2-4e79-3826d7ee04223371bc19319918dee38075c1ba5fcbd000e&dp2=104991&dp3=")
		self.addrList.append("https://global.ymtracking.com/trace?offer_id=5065577&aff_id=104991")
		self.fileList.append("1.mobile.id")
		self.fileList.append("3.mobile.id")
		self.fileList.append("7.mobile.id")
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
		self.loop.run_until_complete(asyncio.wait(self.__start(self.loop)))

	@asyncio.coroutine
	def __start(self, loop):
		async with aiohttp.ClientSession(loop=loop) as session:
			html = yield from self.__fetch(session, 'http://python.org')
			print(html)

	@asyncio.coroutine
	def __fetch(self, session, url):
		print("ffff")


if __name__ == '__main__':
	worker = Worker()
