#!/usr/bin/python

import sys
sys.path.append('..')

import tool

import paramiko
import os
import datetime
import json

from ConfigParser import ConfigParser
from xml.dom import minidom, Node


def init3(cfile):
	
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

	entities = json.loads(cfile)
	for entity in entities:
		name = entity.get('name', '')
		hostname = entity.get('hostname', '')
		port = entity.get('port', 22)
		if port is None:
			port = 22
		ipaddr = entity.get('in_ipaddr', '')
		ex_ipaddr = entity.get('ex_ipaddr', '')
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
			client.connect(hostname = ipaddr, port = port, username = username, password = password)
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
		t = paramiko.Transport((ipaddr, port))
		t.connect(username = username, password = password)
		transports.append(t)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftps[hostname] = sftp
		hosts.append({'name': name, 'hostname': hostname, 'port': port, 'ipaddr': ipaddr, 'ex_ipaddr': ex_ipaddr, 'username': username, 'password': password, 'roles': roles, 'keys': keys})
	print 'Initialize success'
	boot = True
	return hosts


def getNodeValue(node, tagName):
	if node.nodeType <> Node.ELEMENT_NODE:
		return ''
	childs = node.getElementsByTagName(tagName)
	if childs == None or childs.length == 0:
		return ''
	textNode = childs[0].firstChild
	if textNode == None or textNode.nodeType <> Node.TEXT_NODE:
		return ''
	return textNode.nodeValue

def init2(cfile):
	
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

	dom = minidom.parseString(cfile)
	hostNodes = dom.getElementsByTagName('host')
	for node in hostNodes:
		if node.nodeType == Node.ELEMENT_NODE and node.hasAttribute('name'):
			name = node.getAttribute('name')
			hostname = getNodeValue(node, 'hostname')
			port = 22
			port_ = getNodeValue(node, 'port')
			if port_ is not None and port_ <> '':
				port = int(port_)
			ipaddr = getNodeValue(node, 'ipaddr')
			username = getNodeValue(node, 'username')
			password = getNodeValue(node, 'password')
			keys_ = getNodeValue(node, 'keys')
			keys = keys_.split(',')
			
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				client.connect(hostname = ipaddr, port = port, username = username, password = password)
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
			t = paramiko.Transport((ipaddr, port))
			t.connect(username = username, password = password)
			transports.append(t)
			sftp = paramiko.SFTPClient.from_transport(t)
			sftps[hostname] = sftp
			hosts.append({'name': name, 'hostname': hostname, 'port': port, 'ipaddr': ipaddr, 'username': username, 'password': password, 'keys': keys})
	print 'Initialize success'
	boot = True
	return hosts


def init():

	# Load configuration
	
	global boot
	global clients
	global transports
	global sftps
	global hosts 

	if globals().has_key('boot') and boot:
		return hosts

	print 'Beginning initialize'

	cfile = 'cfg.ini'
	cfg = ConfigParser()
	cfg.read(cfile)
	
	boot = False
	clients = {}
	transports = []
	sftps = {}
	hosts = []

	sections = cfg.sections()
	for s in sections:
		hostname = cfg.get(s, 'hostname')
		port = 22
		if cfg.has_option(s, 'port'):
			port = cfg.get(s, 'port')
			if (port is None) or (port == ''):
				port = 22
			else:
				port = int(port) 
		ipaddr = cfg.get(s, 'ipaddr')
		username = cfg.get(s, 'username')
		password = cfg.get(s, 'password')
		keys_ = cfg.get(s, 'keys')
		if keys_ is None:
			keys_ = ''
		keys = keys_.split(',')
		
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(hostname = ipaddr, port = port, username = username, password = password)
		except paramiko.BadHostKeyException, e:
			print 'BadHostKeyException[%s]: %s' % (hostname, e)
			return None
		except paramiko.AutenticationException, e:
			print 'AutenticationException[%s]: %s' % (hostname, e)
			return None
		except paramiko.SSHException, e:
			print 'SSHException[%s]: %s' % (hostname, e)
			return None
		clients[hostname] = client
		t = paramiko.Transport((ipaddr, port))
		t.connect(username = username, password = password)
		transports.append(t)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftps[hostname] = sftp
		hosts.append({'name': s, 'hostname': hostname, 'port': port, 'ipaddr': ipaddr, 'username': username, 'password': password, 'keys': keys})
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

if __name__ == "__main__":
	print 'Beginning to test'
	print '### init ###'
	if init():
		print 'success'
	else:
		print 'fail'
	global boot
	boot = False
	print '### init2(xml) ###'
	f = open('1.xml', 'r')
	if init2(f.read()):
		print 'success'
	else:
		print 'fail'
	f.close()
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
	print '### close ###'
	if close():
		print 'success'
	else:
		print 'fail'
	print 'Test complete'
	



