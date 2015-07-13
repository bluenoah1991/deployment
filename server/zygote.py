#!/usr/bin/python

import os, sys, socket
import pdb

startFlag = '<$'
endFlag = '$>'
sockFile = '/tmp/d2'

def create():
	try:
		if os.fork() > 0:
			os._exit(0)
	except OSError, e:
		print 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
		os._exit(1)

	fsock = open('/var/log/deploy.log', 'w')
	fsock2 = open('/dev/null', 'r')
	sys.stdout = fsock
	sys.stderr = fsock
	sys.stdin = fsock2
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
	if recv is not None:
		recv(sub)
	return buffstr[endIndex + len(endFlag):]

def proc(cmdstr):
	cmd = parse(cmdstr)
	print cmd # TODO
		

if __name__ == '__main__':
	# create()
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	if not os.path.exists(sockFile):
		os.mknod(sockFile)
	if os.path.exists(sockFile):
		os.unlink(sockFile)
		sock.bind(sockFile)
		sock.listen(1) # TODO Multi Client
		buffstr = ''
		while True:
			conn, address = sock.accept()
			data = conn.recv(1024) # Stick package
			pdb.set_trace()
			buffstr = pick(buffstr + data, proc)
		os.unlink(sockFile)
		conn.close()










