#!/usr/bin/python

import sys
sys.path.append('..')

import tool

import paramiko
import os
import datetime
import json

from ConfigParser import ConfigParser

def init(cfile):
	
	# Load configuration
	
	global boot
	global clients
	global transports
	global sftps
	global hosts

	if globals().has_key('boot') and boot:
		return hosts

	print 'Beginning initialize'

	boot = False
	clients = {}
	transports = []
	sftps = {}
	hosts = []

	if isinstance(cfile, basestring):
		cfile = json.loads(cfile)
	for entity in cfile:
		name = entity.get('name', '')
		hostname = entity.get('hostname', '')
		port = entity.get('port', 22)
		if port is None:
			port = 22
		ipaddr = entity.get('in_ipaddr', '')
		ex_ipaddr = entity.get('ex_ipaddr', '')
		ssh_ipaddr = ex_ipaddr
		if ssh_ipaddr is None or len(ssh_ipaddr) == 0:
			ssh_ipaddr = ipaddr
		os = entity.get('os', '')
		username = entity.get('uname', '')
		password = entity.get('passwd', '')
		roles_ = entity.get('roles', '')
		roles = None
		if roles_ is not None:
			roles = roles_.split(',')
		keys_ = entity.get('keys', '')
		keys = None
		if keys_ is not None:
			keys = keys_.split(',')
		
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(hostname = ssh_ipaddr, port = port, username = username, password = password)
		except paramiko.BadHostKeyException, e:
			print 'BadHostKeyException[%s]: %s' % (host, e)
			return None
		except paramiko.AutenticationException, e:
			print 'AutenticationException[%s]: %s' % (host, e)
			return None
		except paramiko.SSHException, e:
			print 'SSHException[%s]: %s' % (host, e)
			return None
		clients[hostname] = client
		t = paramiko.Transport((ssh_ipaddr, port))
		t.connect(username = username, password = password)
		transports.append(t)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftps[hostname] = sftp
		hosts.append({'name': name, 'hostname': hostname, 'port': port, 'ipaddr': ipaddr, 'ex_ipaddr': ex_ipaddr, 'username': username, 'password': password, 'roles': roles, 'keys': keys})
	print 'Initialize success'
	boot = True
	return hosts

def filterRole(key):
	hs_ = []
	for host in hosts:
		if key in host.get('roles', []):
			hs_.append(host)
	return hs_

def filterRoleName(key, name):
	hs_ = []
	for host in hosts:
		if key in host.get('roles', []):
			hs_.append(host.get(name))
	return hs_

def filter(key):
	hs_ = []
	for host in hosts:
		if key in host.get('keys', []):
			hs_.append(host)
	return hs_

def filterName(key, name):
	hs_ = []
	for host in hosts:
		if key in host.get('keys', []):
			hs_.append(host.get(name))
	return hs_

def close():
	global boot

	if globals().has_key('boot') and not boot:
		print 'Please initialize first'
		return 0
	for (host, client) in clients.items():
		client.close()
	for t in transports:
		t.close()
	boot = False
	return 1

def cmd(cmd, all_ = True, *hosts):
	if globals().has_key('boot') and not boot:
		print 'Please initialize first'
		return 0
	if all_:
		for (host, client) in clients.items():
			print '[%s][%s] Execute \'%s\'' % (datetime.datetime.now(), host, cmd)
			stdin, stdout, stderr = client.exec_command(cmd)
			out_ = stdout.read()
			if (out_ is not None) and (out_ <> ''):
				tool.stdout(host, out_)
			err_ = stderr.read()
			if (err_ is not None) and (err_ <> ''):
				tool.stderr(host, err_)
	else:
		for host in hosts:
			if host not in clients:
				continue
			client = clients[host]
			print '[%s][%s] Execute \'%s\'' % (datetime.datetime.now(), host, cmd)
			stdin, stdout, stderr = client.exec_command(cmd)
			out_ = stdout.read()
			if (out_ is not None) and (out_ <> ''):
				tool.stdout(host, out_)
			err_ = stderr.read()
			if (err_ is not None) and (err_ <> ''):
				tool.stderr(host, err_)
	return 1
			

def upload(localFile, remoteFile, all_ = True, *hosts):
	if globals().has_key('boot') and not boot:
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

