#!/usr/bin/python

import sys
sys.path.append('..')

from . import io

import paramiko
import os
import datetime

from ConfigParser import ConfigParser

# Load configuration

cfile = '../cfg.ini'
cfg = ConfigParser()
cfg.read(cfile)

boot = False
clients = {}
transports = []
sftps = {}

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
		clients[host] = client
		t = paramiko.Transport((host, port))
		t.connect(username = user, password = pwd)
		transports.append(t)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftps[host] = sftp
	boot = True
	return 0

def close():
	if not boot:
		print('Please initialize first')
		return -1
	for host, client in clients:
		client.close()
	for t in transports:
		t.close()
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
	else:
		for host in hosts:
			if host not in clients:
				continue
			client = clients[host]
			stdin, stdout, stderr = client.exec_command(cmd)
			out_ = stdout.read()
			if (out_ is not None) and (out_ <> ''):
				io.stdout(host, out_)
			err_ = stderr.read()
			if (err_ is not None) and (err_ <> ''):
				io.stderr(host, err_)
	return 0
			

def upload(localFile, remoteFile, all_ = True, *hosts):
	if not boot:
		print('Please initialize first')
		return -1
	if all_:
		for host, sftp in sftps:
			print '[%s][%s] Beginning to upload file %s' % (datetime.datetime.now(), host, localFile)
			sftp.put(localFile, remoteFile)
			print '[%s][%s] Upload file success %s' % (datetime.datetime.now(), host, localFile)
	else:
		for host in hosts:
			if host not in sftps:
				continue
			sftp = sftps[host]
			print '[%s][%s] Beginning to upload file %s' % (datetime.datetime.now(), host, localFile)
			sftp.put(localFile, remoteFile)
			print '[%s][%s] Upload file success %s' % (datetime.datetime.now(), host, localFile)
	return 0

if __name__ == "__main__":
	print 'Beginning to test'
	print '### exec ###'
	if exec('uname'):
		print 'success'
	else:
		print 'fail'
	if upload('./1.txt', '/tmp/1.txt'):
		print 'success'
	else:
		print 'fail'
	print 'Test complete'
	



