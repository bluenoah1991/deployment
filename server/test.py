#!/usr/bin/python

import sys
sys.path.append('..')

import os, socket
import zygote

sockFile = '/tmp/d2'

if __name__ == '__main__':

	#subb = __import__('demo.subb')
	#demo.subb.subf('sdf')
	#common = __import__('common')
	#hadoop = __import__('hadoop')
	cmd = 'exec "Hello World" arg1 arg2 \'arg3.1 arg3.2\' arg4'
	print zygote.parse(cmd)

	if os.path.exists(sockFile):
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		sock.connect(sockFile)
		sock.send(zygote.pack(cmd))
		sock.close()
