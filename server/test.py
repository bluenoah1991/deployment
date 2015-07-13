#!/usr/bin/python

import sys
sys.path.append('..')

import os, socket
import zygote

sockFile = '/tmp/d2'


if __name__ == '__main__':

	cmd = 'demo.subb.subf.pp hello 123'
	args = zygote.parse(cmd)
	rs = zygote.refcall(args)

	if os.path.exists(sockFile):
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		sock.connect(sockFile)
		sock.send(zygote.pack(cmd))
		sock.close()
