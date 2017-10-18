#!/usr/bin/python
#coding=utf-8
from datetime import datetime, timedelta
from pymongo import MongoClient, errors

class MongoQueue():
	
	def __init__(self, db, collection, timeout=150): #初始mongodb连接
		self.client = MongoClient('localhost', 27017)
		self.Client = self.client[db]
		self.db = self.Client[collection]
		self.timeout = timeout
		self.OUTSTANDING = 2 # 初始状态
		self.PROCESSING = 3 # 正在下载状态
		self.COMPLETE = 4 # 下载完成状态

	def __bool__(self):
		"""
		$ne means not match
		"""
		oRecord = self.db.find({'status': self.OUTSTANDING})
		pRecord = self.db.find({'status': self.PROCESSING})
		return True if oRecord or pRecord  else False
	
	def push(self, url, title): # 这个函数用来添加新的URL进队列,$ne表示不匹配
		try:
			self.db.insert_one({'_id': url, 'status': self.OUTSTANDING, '主题': title})
			print url, '插入队列成功'
		except errors.DuplicateKeyError as e: #报错则代表已经存在于队列之中了
			print url, '已经存在于队列中了'
			pass

	def pushJiandan(self, summary, sTitle, url):
		# 此函数用于把爬去到的煎蛋网内容写入数据库
		if self.db.find({'简介': summary}).count() < 1:
			self.db.insert_one({
				'简介': summary,
				'小标题': sTitle,
				'主题链接': url
				}
			)
			print url, '插入数据库成功'
		else:
			# 代表已经存在于数据库之中了
			print url, '已经存在于数据库中了'

	def pop(self):
		"""
		这个函数会查询队列中的所有状态为OUTSTANDING的值，
        更改状态，（query后面是查询）（update后面是更新）
        并返回_id（就是我们的ＵＲＬ），MongDB好使吧，^_^
        如果没有OUTSTANDING的值则调用repair()函数重置所有超时的状态为OUTSTANDING，
        $set是设置的意思，和MySQL的set语法一个意思
		"""
		time = datetime.now()
		record = self.db.find_one_and_update(
			{'status': self.OUTSTANDING},
			{'$set': {'status': self.PROCESSING, 'timestamp': time}}
		)
		if record:
			return record['_id']
		else:
			self.repair()
			raise KeyError

	def pop_title(self, url):
		record = self.db.find_one({'_id': url})
		return record['主题']

	def peek(self):
		"""这个函数是取出状态为OUTSTANDING的文档并返回_id(URL)"""
		record = self.db.find_one({'status': self.OUTSTANDING})
		if record:
			return record['_id']

	def complete(self, url):
		"""这个函数是更新已完成的URL完成"""
		self.db.update_one({'_id': url}, {'$set': {'status': self.COMPLETE}})

	def repair(self):
		#这个函数是重置状态
		print 'repair'
		record = self.db.find({'status':{'$ne':self.COMPLETE}}, limit=1)[0]
		if record:
			if (datetime.now() - record['timestamp']) > timedelta(seconds=self.timeout):
				self.db.find_one_and_update({'_id': record['_id']}, {'$set':{'status':self.OUTSTANDING}})
				print '重置URL状态', record['_id']
			else:
				print '重置时间还没到,当前时间间隔为:%s' % (datetime.now() - record['timestamp'])
		else:
			print '全部爬取完成，结束程序.'
	def count(self):
		# 数据库内容的数量
		return self.db.count()

	def clear(self):
		"""这个函数只有第一次才调用、后续不要调用、因为这是删库啊！"""
		self.db.drop()
		print 'finished'

# p = MongoQueue('jiandan', 'jdlinks')
# p.clear()