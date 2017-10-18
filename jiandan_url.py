#coding=utf-8

from mongodb_queue import MongoQueue

jiandan_queue = MongoQueue('jiandan', 'jdlinks')
url = 'http://jandan.net/page/'
def start():
	for num in range(1, 2484):
		title = 'jiandanPage:' + str(num)
		jdurl = url+str(num)
		jiandan_queue.push(jdurl, title)
		# print title

if __name__ == '__main__':
	start()