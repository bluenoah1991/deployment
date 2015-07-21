#!/usr/bin/python

import sys
sys.path.append('..')

import os, socket
import zygote

sockFile = '/tmp/d2'


if __name__ == '__main__':

	f = open('cfg.json', 'r')
	cfg = f.read()
	cmd = "hadoop.install.main '%s'" % cfg

	if os.path.exists(sockFile):
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		sock.connect(sockFile)
		sock.send(zygote.pack(cmd))
		sock.close()
