#!python3
# encoding: utf-8

import sys
import socket
import re
from multiprocessing.dummy import Pool as ThreadPool

socket.setdefaulttimeout(1)


def scan(host, threads = 10):
	ip = host
	pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")
	if pattern.match(host) is None:
		ip = socket.gethostbyname(host)

	pool = ThreadPool(threads)
	results = pool.map(do_scan, map(lambda port: (ip, port), range(1, 65536, 1)))
	pool.close()
	pool.join()

	return map(lambda r: r[0], filter(lambda r: r[1], results))

# do_scan((ip, port))
def do_scan(sock):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex(sock)
	s.close()
	return [sock[1], result == 0]


if __name__ == '__main__':
	if len(sys.argv) == 2:
		ports = scan(sys.argv[1], 20)
		for port in ports:
			print("{} open".format(port))
	else:
		print("{} ip".format(sys.argv[0]))
