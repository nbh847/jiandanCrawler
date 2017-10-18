#!/usr/bin/python
#coding=utf-8

from bs4 import BeautifulSoup
import sys, time, pickle, requests, re, random
import pymongo

class Proxy(object):
	"""docstring for proxy"""
	def __init__(self):
		#--------------proxy-------------
		
		self.testUrl = 'http://jandan.net/page/'
		# 设置MongoDB连接信息
		self.client = pymongo.MongoClient('localhost', 27017)
		self.ipDB = self.client['proxy']
		self.ipConn = self.ipDB['project_ip']

	def isAlive(self, ip):
		# 判断ip是否有效
		proxy = {'http': ip, 'https': ip}
		try:
			requests.get(self.testUrl + str(random.randint(1,10)), headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0', 'Connection': 'keep-alive'}, timeout=8, proxies=proxy)
		except Exception as e:
			print 'bad ip %s' % ip
			return False
		return True

	def removeIP(self, ip):
		self.ipConn.remove({'proxy': ip})
		print '已经移除ip', ip

	def count(self):
		# 返回数据库里ip的数量
		return self.ipConn.count()

	def testAlive(self):
		# 检查代理的可用情况，移除其中不可用的ip
		for ip in self.ipConn.find():
			# print ip['proxy']
			if not self.isAlive(ip['proxy']):
				print 'ip %s is not alive' % ip['proxy']
				self.removeIP(ip['proxy'])
				print 'remove ip %s successfully..' % ip['proxy']
			else:
				print 'ip %s is alive' % ip['proxy']

	def xiciProxy(self):
		# 西刺代理
		xiciUrl = 'http://www.xicidaili.com/nn/'
		try:
			req = requests.get(xiciUrl + str(random.randint(1,100)), timeout=8, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'})
			if req.status_code != 200:
				print 'response code: %s' % str(req.status_code)
				print '被西刺代理禁了，稍后再试'
				return
		except:
			print '被西刺代理禁了，稍后再试'
			return
		print self.url + str(random.randint(1,100))
		result = req.content
		soup = BeautifulSoup(result, 'lxml')
		oddIP = soup.find_all(class_="odd")
		evenIP = soup.find_all('tr', class_="")
		allIP = [] # store all proxy IP

		#-------get all ip-------------
		for odd in oddIP:
			item = odd.get_text("|")
			ip = item.split("|")[2]
			port = item.split("|")[4]
			if self.isAlive(ip+':'+port):
				allIP.append(ip+':'+port)
				print 'ip %s is finished...' % ip

		for even in evenIP:
			item = even.get_text("|")
			ip = item.split("|")[2]
			port = item.split("|")[4]
			if port.isdigit():
				if self.isAlive(ip+':'+port):
					allIP.append(ip+':'+port)
					print 'ip %s is finished...' % ip
		time.sleep(2)
		return allIP

	def kuaiProxy(self):
		# 快代理
		kuaidailiUrl = 'http://www.kuaidaili.com/free/inha/%s/'
		try:
			req = requests.get(kuaidailiUrl % str(random.randint(2,100)), timeout=8, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'})
			if req.status_code != 200:
				print 'response code: %s' % str(req.status_code)
				print '被快代理禁了，稍后再试'
				return
		except:
			print '被快代理禁了，稍后再试'
			return
		print kuaidailiUrl % str(random.randint(1, 100))
		print req.status_code
		content = req.text
		soup = BeautifulSoup(content, 'lxml')
		ips = soup.find_all(attrs={'data-title': "IP"})
		ports = soup.find_all(attrs={'data-title': "PORT"})
		ipList = [] # 储存ip
		portList = [] # 储存端口号
		for ip in ips:
			ipList.append(ip.get_text())
		for port in ports:
			portList.append(port.get_text())
		allIP = []
		for i in range(len(ipList)):
			allIP.append(ipList[i]+':'+portList[i])
		time.sleep(2)
		return allIP

	def sixIP(self):
		# 66ip
		sixUrl = 'http://www.66ip.cn/%s.html'
		try:
			req = requests.get(sixUrl % str(random.randint(2,100)), timeout=8, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'})
			if req.status_code != 200:
				print 'response code: %s' % str(req.status_code)
				print '被66ip代理禁了，稍后再试'
				return
		except:
			print '被66ip代理禁了，稍后再试'
			return
		print sixUrl % str(random.randint(1, 100))
		print req.status_code
		content = req.text
		soup = BeautifulSoup(content, 'lxml')
		items = soup.find_all("td")
		ips = []
		ports = []
		allIP = []
		for it in items:
			item = it.get_text()
			if item[0].isdigit() and item[-1].isdigit():
				if len(item) > 6:
					# ip
					ips.append(item)
				else:
					# port
					ports.append(item)
		try:	
			for i in range(len(ips)):
				allIP.append(ips[i]+':'+ports[i])
		except Exception as e:
			print e
			print '结束本个网站代理ip的获取'
			return 
		time.sleep(2)
		return allIP

	def yunProxy(self):
		# yunProxy
		yunUrl = 'http://www.ip3366.net/free/?stype=1&page=%s'
		try:
			req = requests.get(yunUrl % str(random.randint(1,7)), timeout=8, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'})
			if req.status_code != 200:
				print 'response code: %s' % str(req.status_code)
				print '被云代理禁了，稍后再试'
				return
		except:
			print '被云代理禁了，稍后再试'
			return
		print yunUrl % str(random.randint(1, 7))
		print req.status_code
		content = req.text
		soup = BeautifulSoup(content, 'lxml')
		items = soup.find_all("td")
		ips = []
		ports = []
		allIP = []
		for it in items:
			item = it.get_text()
			if item[0].isdigit() and item[-1].isdigit() and '/' not in item:
				if len(item) > 6:
					# ip
					ips.append(item)
				else:
					# port
					ports.append(item)
		for i in range(len(ips)):
			allIP.append(ips[i]+':'+ports[i])
		time.sleep(2)
		return allIP

	# @staticmethod
	def storeIP(self):
		# 将ip存到数据库中
		xici = self.xiciProxy()
		kuai = self.kuaiProxy()
		six = self.sixIP()
		yun = self.yunProxy()
		allIP = []
		# 将获取到的ip集中处理
		if xici is not None:
			for x in xici:
				allIP.append(x)
		if kuai is not None:
			for k in kuai:
				allIP.append(k)
		if six is not None:
			for s in six:
				allIP.append(s)
		if yun is not None:
			for y in yun:
				allIP.append(y)
		#---------------------
		# insert all IP to db if the ip is not duplicate
		for i in allIP:
			if self.isAlive(i) and self.ipConn.find({'proxy': i}).count() < 1:
				# 如果ip不在数据库中并且可用，则储存
				self.ipConn.insert_one({'proxy': i})
				print 'insert %s to db successfully...' % i
			else:
				print '重复ip'

	def getIP(self, num = 10):
		self.testAlive()
		# 前检查代理的可用个数
		while True:
			if self.count() < 10:
				print 'ip个数为%s个,少于10个，继续获取' % self.count()
				self.storeIP()
			else:
				print 'ip够了，结束.'
				break
		# 取出数据库中的ip，默认是取出10个
		nIP = []
		for ip in self.ipConn.find(limit = num):
			nIP.append(ip['proxy'].encode('utf8'))
		return nIP

	def test(self):
		print self.url

	def run(self):
		# print self.yunProxy()
		# print self.yunProxy()
		self.storeIP()
		# print self.count()
		# print self.count()
		# print self.getIP()
		# self.testAlive()
		# self.test()
		# print type(self.getIP()[0])

myProxy = Proxy()
# myProxy.run()