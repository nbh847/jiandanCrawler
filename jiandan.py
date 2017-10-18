#!/usr/bin/python
#coding=utf-8
#douban crowler
from __future__ import unicode_literals
import requests, time, re, random, pymongo, threading
from bs4 import BeautifulSoup
import multiprocessing
from mongodb_queue import MongoQueue
from Download import request

SLEEP_TIME = 1

def jiandan(max_threads=10):

	crawl_queue = MongoQueue('jiandan', 'jdlinks') # 这个是我们获取URL的队列
	jd_queue = MongoQueue('jiandan', 'project_jiandan') #这是储存在数据库的队列

	def pageurl_crawler():
		while True:
			try:
				url = crawl_queue.pop()
				print url
			except KeyError:
				print '队列没有数据'
				break
			else:
				allTitleUrl = [] #主题链接
				allLittleData = [] #简介
				smallTitle = [] # 小标题

				content = request.get(url, 3).text
				soup = BeautifulSoup(content, 'lxml')
				#--------------all url and summary------------------
				title = soup.find_all(href=re.compile('jandan.net'), target="_blank")
				for i in title:
					if len(i.get_text()) != 0:
						allTitleUrl.append(i['href'])
						allLittleData.append(i.get_text())
				#-------------little title---------------
				sTitle = soup.find_all(class_="time_s")
				for t in sTitle:
					smallTitle.append(t.get_text())
				#----------insert data into mongodb------
				for i in range(len(smallTitle)):
					smTitle = smallTitle[i]
					urls = allTitleUrl[i]
					summary = allLittleData[i]
					jd_queue.pushJiandan(summary, smTitle, urls)
				crawl_queue.complete(url)
				print '完成本页数据入库'
				print '数据库内容的数量: %s' % jd_queue.count()

	threads = [] #线程列表
	while threads or crawl_queue:
		#这儿crawl_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
        #threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
		for thread in threads:
			if not thread.is_alive(): #is_alive判断该线程是否存活,不是则在队列中删掉
				threads.remove(thread)
		while len(threads) < max_threads or crawl_queue.peek(): # 线程池中的线程少于max_threads 或者 crawl_qeue时
			thread = threading.Thread(target=pageurl_crawler) # 创建线程
			thread.setDaemon(True) #设置守护线程
			thread.start() #启动线程
			threads.append(thread) #添加进线程队列
		time.sleep(SLEEP_TIME)

def process_crawler():
	process = []
	p = multiprocessing.Pool()
	n = multiprocessing.cpu_count()
	print '将会启动进程数为: ', n
	for i in range(n):
		p = multiprocessing.Process(target=jiandan) #创建进程
		p.start() #启动进程
		process.append(p) # 添加进进程队列
	for p in process:
		p.join() # 等待进程队列里面的进程结束
	# for i in range(n):
	# 	p.apply_async(jiandan)
	# p.close()
	# p.join()
		
if __name__ == '__main__':
	process_crawler()