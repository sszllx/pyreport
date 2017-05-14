
import aiohttp
import asyncio
import collections
import requests
import random
import time
import urllib

class Holder:
	def __init__(self):
		self.addrList = collections.deque()
		self.fileList = collections.deque()
		self.init()

	def init(self):
		# ofo
		# self.addrList.append("https://lnk0.com/Mt8Edc?transaction_id=fb31665d0-832e-a698-d42c965aaf3f572602333e4cc8b0e52d9f0161f6b12000b&affiliate_id=104991&aff_sub8=")
		self.addrList.append("https://global.ymtracking.com/trace?offer_id=5107479&aff_id=104991")
		# elema
		# self.addrList.append("http://network.adsmarket.com/click/j2dxlV-hqZqMY26bYMp6w4iQbJZeoYOVjWqYnGShfZuNkGqdYaGAmLdibZhmoYOU?dp=475b7bf70-7fd2-4e79-3826d7ee04223371bc19319918dee38075c1ba5fcbd000e&dp2=104991&dp3=")
		self.addrList.append("https://global.ymtracking.com/trace?offer_id=5065577&aff_id=104991")
		self.fileList.append("1.mobile.id")
		self.fileList.append("3.mobile.id")
		self.fileList.append("7.mobile.id")

	def getFileList(self):
		return self.fileList

	def getAddr(self):
		return self.addrList

def send_request(holder):
	ua_str = ["Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
			  "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25",
			  "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
			  "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11A465 Twitter for iPhone"]
	headers = {"User-Agent":""}

	for fi in holder.getFileList():
		with open(fi, 'rt') as f:
			for line in f:
				time.sleep (0.2)
				proxies = {}
				proxies['https'] = get_proxy()
				for item in holder.getAddr():
					print (item + "&idfa=" + line)
					headers['User-Agent'] = ua_str[random.randint(0, 3)]
					# print (headers)
					# try:
						# response = requests.get(item + "&idfa=" + line, proxies=proxies, 
						# 						headers=headers,
						# 						allow_redirects=True,
						# 						timeout=10)
						# response = requests.get("https://global.ymtracking.com/trace?offer_id=5065577&aff_id=104991&idfa=3655C6E7-D159-4370-8840-081C8F001654", proxies=proxies, 
						# 						headers=headers,
						# 						allow_redirects=True,
						# 						timeout=10)
						# response = requests.get("https://global.ymtracking.com/trace?offer_id=5107479&aff_id=104991&idfa=3655C6E7-D159-4370-8840-081C8F001654", proxies=proxies, 
						# 						headers=headers,
						# 						allow_redirects=True,
						# 						timeout=10)
						# if (response.status_code == 302):
						# 	print(response.location)
						
					# except Exception as e:
					# 	print (e)

async def get_status(url, id):
    r = await aiohttp.get(url)
    print(r.status, id)
    r.close()

def do_work():
	tasks = []
	holder = Holder()

	for i in range(100):
    	tasks.append(asyncio.ensure_future(get_status('https://api.github.com/events', id=i)))

	# while 1:
	# 	send_request(holder)
			        

def get_proxy():
	order = "70d8ff78674398a42e90a879683582fd"
	apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
	try:
		res = urllib.request.urlopen(apiUrl).read().decode().strip("\n")
		# print("ips:" + res)
		return res
	except Exception as e:
		print(e)

if __name__ == '__main__':
	# do_work()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()