#!/usr/bin/python

import sys
sys.path.append('..')

import io

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
	print 'Beginning initialize'
	global boot
	hosts = []
	sections = cfg.sections()
	for s in sections:
		host = cfg.get(s, 'host')
		port = 22
		if cfg.has_option(s, 'port'):
			port = cfg.get(s, 'port')
			if (port is None) or (port == ''):
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
			print 'BadHostKeyException[%s]: %s' % (host, e)
			return None
		except AutenticationException, e:
			print 'AutenticationException[%s]: %s' % (host, e)
			return None
		except SSHException, e:
			print 'SSHException[%s]: %s' % (host, e)
			return None
		clients[host] = client
		t = paramiko.Transport((host, port))
		t.connect(username = user, password = pwd)
		transports.append(t)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftps[host] = sftp
		hosts.append(host)
	boot = True
	print 'Initialize success'
	return hostnames

def close():
	if not boot:
		print 'Please initialize first'
		return 0
	for (host, client) in clients.items():
		client.close()
	for t in transports:
		t.close()
	return 1

def cmd(cmd, all_ = True, *hosts):
	if not boot:
		print 'Please initialize first'
		return 0
	if all_:
		for (host, client) in clients.items():
			print '[%s][%s] Execute \'%s\'' % (datetime.datetime.now(), host, cmd)
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
	return 1
			

def upload(localFile, remoteFile, all_ = True, *hosts):
	if not boot:
		print 'Please initialize first'
		return 0
	if all_:
		for (host, sftp) in sftps.items():
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
	return 1

if __name__ == "__main__":
	print 'Beginning to test'
	print '### init ###'
	if init():
		print 'success'
	else:
		print 'fail'
	print '### exec ###'
	if cmd('uname'):
		print 'success'
	else:
		print 'fail'
	print '### exec sudo ###'
	if cmd('sudo uname'):
		print 'success'
	else:
		print 'fail'
	print '### upload ###'
	if upload('./1.txt', '/tmp/1.txt'):
		print 'success'
	else:
		print 'fail'
	print '### upload sudo ###'
	if upload('./1.txt', '/tmp/1.txt') and cmd('sudo cp /tmp/1.txt /usr/local/1.txt'):
		print 'success'
	else:
		print 'fail'
	print 'Test complete'
	



