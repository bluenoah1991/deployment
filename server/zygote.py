#!/usr/bin/python

import sys
sys.path.append('..')

import os, socket
# import pdb

startFlag = '<$'
endFlag = '$>'
sockFile = '/tmp/d2'

class Unbuffered(object):
	def __init__(self, stream):
		self.stream = stream
	def write(self, data):
		self.stream.write(data)
		self.stream.flush()
	def __getattr__(self, attr):
		return getattr(self.stream, attr)

def refcall(args):
	if args is None or len(args) == 0:
		return -1
	ns = []
	fullpath = ''
	path = ''
	for i, ch in enumerate(args[0]):
		if ch == '.':
			ns.append((path, fullpath))
			path = ''
		else:
			path = path + ch
		fullpath = fullpath + ch
	ns.append((path, fullpath))
	root = globals().get(ns[0][0])
	if root is None:
		try:
			root = __import__(ns[0][0]) # Import Error
		except ImportError, e:
			return -1
	current = root
	for _ in ns[1:]:
		if _[0] not in dir(current):
			try:
				__import__(_[1]) # Import Error
			except ImportError, e:
				return -1
		current = getattr(current, _[0])
	if not callable(current):
		return -1
	try:
		current(*args[1:]) # Call Failure
	except TypeError, e:
		return -1

def create():
	try:
		if os.fork() > 0:
			os._exit(0)
	except OSError, e:
		print 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
		os._exit(1)

	fsock = open('/var/log/deploy.log', 'w')
	fsock2 = open('/dev/null', 'r')
	fsock3 = open('/var/log/deploy.err', 'w')
	sys.stdout = Unbuffered(fsock)
	sys.stdin = fsock2
	sys.stderr = Unbuffered(fsock3)
	os.chdir('/')
	os.setsid()
	os.umask(0)

def parse(cmd):
	if cmd is None:
		return None
	args = []
	seg = ''
	flag = ''
	for i, ch in enumerate(cmd):
		if flag == '' and ch == '"':
			flag = '"'
			continue
		if flag == '' and ch == "'":
			flag = "'"
			continue
		if (flag == '"' and ch == '"') or (flag == "'" and ch == "'"):
			args.append(seg)
			seg = ''
			flag = ''
			continue
		if flag == '' and ch == ' ':
			if seg is not None and seg <> '':
				args.append(seg)
				seg = ''
			continue
		seg = seg + ch
	if seg is not None and seg <> '':
		args.append(seg)
		seg = ''
	return args

def pack(cmd):
	return startFlag + cmd + endFlag
		
def pick(buffstr, recv):
	if buffstr is None or buffstr == '':
		return buffstr
	if not buffstr.startswith(startFlag):
		startIndex = buffstr.find(startFlag)
		if startIndex == -1:
			return buffstr
		buffstr = buffstr[startIndex:]
	endIndex = buffstr.find(endFlag)
	if endIndex == -1:
		return buffstr
	sub = buffstr[0: endIndex + len(endFlag)]
	sub = sub[len(startFlag): len(sub) - len(endFlag)]
	if recv is not None and callable(recv):
		recv(sub)
	return buffstr[endIndex + len(endFlag):]

def proc(cmd):
	args = parse(cmd)
	print 'exec: "%s"' % cmd
	refcall(args) # Stdout redirect

def acceptEvent(conn):
	buffstr = ''
	while True:
		data = conn.recv(1024) # Stick package
		#pdb.set_trace()
		if not len(data) : break
		buffstr = pick(buffstr + data, proc)
	conn.close()

if __name__ == '__main__':

	if '-d' in sys.argv:
		create()

	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	if not os.path.exists(sockFile):
		os.mknod(sockFile)
	if os.path.exists(sockFile):
		os.unlink(sockFile)
		sock.bind(sockFile)
		sock.listen(1) # TODO Multi Client
		while True:
			conn, address = sock.accept()
			acceptEvent(conn)
		os.unlink(sockFile)
		conn.close()






