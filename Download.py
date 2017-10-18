#coding=utf-8

import requests
import re
import random
import time
from Proxy import myProxy

class download():

	def __init__(self):

		self.iplist = myProxy.getIP() # list用来存放我们从数据库获取到的IP

		self.user_agent_list = [
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
			"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"
			]

	def get(self, url, timeout, proxy=None, num_retries=6): ##给函数一个默认参数proxy为空
		UA = random.choice(self.user_agent_list) ###从self.user_agent_list中随机取出一个字符串
		headers = {'User-Agent': UA} ##构造成一个完整的User-Agent

		if proxy == None : ##当代理为空时，不使用代理获取response
			try:
				response = requests.get(url, headers=headers, timeout=timeout) #伪装成浏览器
				if response.status_code == 200:
					return response
				else:
					# 当ip数量少于1个时，再次获取ip
					if len(self.iplist) < 3:
						self.iplist = myProxy.getIP()
					IP = random.choice(self.iplist)
					proxy = {'http': IP, 'https': IP}
					return self.get(url, timeout, proxy,)
			except:#如过上面的代码执行报错则执行下面的代码
				
				if num_retries > 0: ##num_retries是我们限定的重试次数
					time.sleep(10) ##延迟十秒
					print u'获取网页出错，10S后将获取倒数第：', num_retries, u'次'
					return self.get(url, timeout, num_retries-1) #调用自身 并将次数减1
				else:
					print u'开始使用代理'
					time.sleep(10)
					# 当ip数量少于1个时，再次获取ip
					if len(self.iplist) < 1:
						self.iplist = myProxy.getIP()
					IP = random.choice(self.iplist)
					proxy = {'http': IP, 'https': IP}
					return self.get(url, timeout, proxy,) #代理不为空的时候
		else: #当代理不为空
			try:
				# 当ip数量少于1个时，再次获取ip
				if len(self.iplist) < 1:
					self.iplist = myProxy.getIP()
				IP = random.choice(self.iplist)
				proxy = {'http': IP, 'https': IP}
				response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
				if response.status_code == 200:
					return response
				else:
					print 'ip %s is invalid, remove it' % IP
					myProxy.removeIP(IP)
					self.iplist.remove(IP)
					if num_retries > 0:
						time.sleep(10)
						# 当ip数量少于1个时，再次获取ip
						if len(self.iplist) < 1:
							self.iplist = myProxy.getIP()
						IP = random.choice(self.iplist)
						proxy = {'http': IP, 'https': IP}
						print u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次'
						print u'当前代理是: ', proxy
						return self.get(url, timeout, proxy, num_retries-1)
					else:
						print u'代理也不好使了！取消代理'
						return self.get(url, 3)
			except:
				print 'ip %s is invalid, remove it' % IP
				if IP in self.iplist:
					myProxy.removeIP(IP)
					self.iplist.remove(IP)
				if num_retries > 0:
					time.sleep(10)
					# 当ip数量少于1个时，再次获取ip
					if len(self.iplist) < 1:
						self.iplist = myProxy.getIP()
					IP = random.choice(self.iplist)
					proxy = {'http': IP, 'https': IP}
					print u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次'
					print u'当前代理是: ', proxy
					return self.get(url, timeout, proxy, num_retries-1)
				else:
					print u'代理也不好使了！取消代理'
					return self.get(url, 3)
		time.sleep(1)

request = download()
# print request.get('http://jandan.net/page/1', 3)
# print type(request.iplist[0])