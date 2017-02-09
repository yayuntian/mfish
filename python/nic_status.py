#!/usr/bin/env python
######################################
#nic_traffic.pl => nic_status.py
#HuiLi
#2015-05-21
######################################
import sys
import time
import os
import re
import copy
#import threading
import signal

def handler(signum, frame):
    print ""
    exit(1)


class Status(object):
	def __init__(self):
		self.color = {
				'purple': '\033[1;35;2m',
				'red': '\033[1;31;2m',
				'green': '\033[1;32;2m',
				'default': '\033[0;0m'
		}
		self.freshtime = 1
		self.maxnic = 4
		self.width = 10
		self.G = 1024 * 1024 * 1024
		self.M = 1024 * 1024
		self.K = 1024
		self.commlen = 120

	def __printf(self, string):
		sys.stdout.write(string)
		sys.stdout.flush()

	def __purple(self, string):
		return '%s%s%s' %(self.color['purple'], string, self.color['default'])

	def __red(self, string):
		return '%s%s%s' %(self.color['red'], string, self.color['default'])

	def __green(self, string):
		return '%s%s%s' %(self.color['green'], string, self.color['default'])
	
	def __theme(self, front, end, num, bool):
		num = self.__int2str(num)
		if bool == 'wrong':
			self.__printf('| ' + front + self.__red(num) + end + '\n')
		elif bool == 'right':
			self.__printf('| ' + front + self.__green(num) + end + '   ')
		else:
			print 'color flag error'
			sys.exit(0)
	
	def __gettime(self):
		nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
		return nowtime

	def __parser(self, nic):
		data = {}
		pattern_pkt = 'RX packets:(\d+)?.*dropped:(\d+)?'
		pattern_byte = 'RX bytes:(\d+)?'
		rxlist = []
		try:
			nicpf = os.popen('ifconfig %s | grep RX' %nic)
		except IOError, e:
			sys.exit(0)
		for eachLine in nicpf:
			eachLine = eachLine.strip()
			rxlist.append(eachLine)
		info_pkt = re.search(pattern_pkt, rxlist[0])
		info_byte = re.search(pattern_byte, rxlist[1])
		if info_pkt is not None:
			data['packets'] = int(info_pkt.group(1))
			data['dropped'] = int(info_pkt.group(2))
		if info_byte is not None:
			data['bytes'] = int(info_byte.group(1))
		return data
	
	def __int2str(self, num):
		if num > self.G:
			num = '%.1f G' %(num * 1.0 / self.G)
		elif num > self.M:
			num = '%.1f M' %(num * 1.0 / self.M)
		elif num > self.K:
			num = '%.1f K' %(num * 1.0 / self.K)
		else:
			num = '%.1f  ' %(num * 1.0)
		return num

	def __show(self, nic, b, p, a, d):
		self.__printf(self.__gettime())
		self.__printf(self.__purple(nic.center(self.width)))
		self.__theme('bps: ', 'bits/s', b, 'right')
		self.__theme('packets: ', 'pkts/s', p, 'right')
		self.__theme('avg: ', 'bytes', a, 'right')
		self.__theme('dropped: ', 'pkts/s', d, 'wrong')
	
	def process(self, nic, number):
		self.__count(nic, number)

	def __count(self, nic, number):
		global b0, b1, b2, b3, p0, p1, p2, p3, d0, d1, d2, d3, a 
		dict = self.__parser(nic)
		if number == 0:
			a = 0 if (dict['packets'] - p0) == 0 else (dict['bytes'] - b0) / (dict['packets'] - p0)
			self.__show(nic, 8 * (dict['bytes'] - b0), dict['packets'] - p0, a, dict['dropped'] - d0)
			b0, p0, d0 = dict['bytes'], dict['packets'], dict['dropped']
		elif number == 1:
			a = 0 if (dict['packets'] - p1) == 0 else (dict['bytes'] - b1) / (dict['packets'] - p1)
			self.__show(nic, 8 * (dict['bytes'] - b1), dict['packets'] - p1, a, dict['dropped'] - d1)
			b1, p1, d1 = dict['bytes'], dict['packets'], dict['dropped']
		elif number == 2:
			a = 0 if (dict['packets'] - p2) == 0 else (dict['bytes'] - b2) / (dict['packets'] - p2)
			self.__show(nic, 8 * (dict['bytes'] - b2), dict['packets'] - p2, a, dict['dropped'] - d2)
			b2, p2, d2 = dict['bytes'], dict['packets'], dict['dropped']
		elif number == 3:
			a = 0 if (dict['packets'] - p3) == 0 else (dict['bytes'] - b3) / (dict['packets'] - p3)
			self.__show(nic, 8 * (dict['bytes'] - b3), dict['packets'] - p3, a, dict['dropped'] - d3)
			b3, p3, d3 = dict['bytes'], dict['packets'], dict['dropped']
		else:
			print 'Sorry, nic argv more than maxnic !'
			sys.exit(0)

b0 = b1 = b2 = b3 = 0
p0 = p1 = p2 = p3 = 0
d0 = d1 = d2 = d3 = 0

if __name__ == '__main__':
	signal.signal(signal.SIGINT, handler)
	status = Status()
	while 1:
		number = 0
		print '#' * status.commlen
		for nic in sys.argv[1:]:
			#t = threading.Thread(target = status.process(nic, number))
			#t.start()
			status.process(nic, number)
			number = (number + 1) % status.maxnic 
		time.sleep(status.freshtime)
