#!python3
# encoding: utf-8

import requests
import sys
import re
from multiprocessing.dummy import Pool as ThreadPool


def ip2long(ip):
	tmp = [int(v) for v in ip.split('.')]
	l = 0
	for v in tmp:
		l = (l << 8) | v
	return l

def long2ip(l):
	tmp = []
	while l > 0:
		tmp.append(l % 256)
		l = l >> 8
	tmp.reverse()
	return '.'.join(["{}".format(v) for v in tmp])

def scan(begin, end, port):
	start = ip2long(begin)
	to = ip2long(end)
	urls = [generate(long2ip(v), port) for v in range(start, to, 1)]
	urls.append(generate(long2ip(to), port))

	pool = ThreadPool(10)
	results = pool.map(check, urls)
	pool.close()
	pool.join()

	return map(lambda it: it[1], filter(lambda it: it[0] == 'Y', results))

# Server: DNVRS-Webs
def check(url):
	print('check', url)
	try:
		r = requests.get(url)
		if r.status_code == requests.codes.OK:
			return ['Y', url]
		else:
			return ['N', url]
	except:
		return ['F', url]

def generate(ip, port = 80):
	scheme = 'https' if port == 443 else 'http'
	url = "{}://{}{}/".format(scheme, ip, ('' if port == 80 or port == 443 else ":{}".format(port)))
	return url


if __name__ == '__main__':
	argc = len(sys.argv)
	if len(sys.argv) != 4:
		print("usage: {} begin-ip end-ip port\npython3 {} 124.125.126.1 124.125.127.255 80\n")
	else:
		urls = scan(sys.argv[1], sys.argv[2], sys.argv[3])
		print(urls)

