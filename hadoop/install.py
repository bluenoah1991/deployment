#!/usr/bin/python

import sys
sys.path.append('..')

import common.io

import paramiko
import os
import datetime

from ConfigParser import ConfigParser

# Load configuration

cfile = 'cfg.ini'
cfg = ConfigParser()
cfg.read(cfile)

boot = False
clients = {}

def init():
	sections = cfg.sections()
	for s in sections:
		host = cfg.get(s, 'host')
		port = cfg.get(s, 'port')
		if (port is None) or (port == '')):
			port = 22
		else:
			port = int(port) 
		user = cfg.get(s, 'user')
		pwd = cfg.get(s, 'pwd')
		
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(hostname = host, port = port, username = user, password = pwd)
		except BadHostKeyException, e:
			print('BadHostKeyException[%s]: %s' % (host, e)
			return -1
		except AutenticationException, e:
			print('AutenticationException[%s]: %s' % (host, e)
			return -1
		except SSHException, e:
			print('SSHException[%s]: %s' % (host, e)
			return -1
		clients[s] = client
	boot = True
	return 0

def exec(cmd, all_ = True, *hosts):
	if not boot:
		print('Please initialize first')
		return -1
	if all_:
		for host, client in clients:
			stdin, stdout, stderr = client.exec_command(cmd)
			out_ = stdout.read()
			if (out_ is not None) and (out_ <> ''):
				io.stdout(host, out_)
			err_ = stderr.read()
			if (err_ is not None) and (err_ <> ''):
				io.stderr(host, err_)







