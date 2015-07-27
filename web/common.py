#!/usr/bin/python

import sys, os, datetime, json
import paramiko

def stdout_(host, out):

	sys.stdout.write('%s say:\n' % host)
	sys.stdout.write(out)

def stderr_(host, out):

	sys.stdout.write('%s say(stderr):\n' % host)
	sys.stdout.write(out)

def join(_file_, filename):

	path = os.path.split(os.path.realpath(_file_))[0]
	return os.path.join(path, filename)

class SSH(object):

	def cmd(self, cmd, all_ = True, *hosts):
		if all_:
			for (host, client) in self.clients.items():
				print '[%s][%s] Execute \'%s\'' % (datetime.datetime.now(), host, cmd)
				stdin, stdout, stderr = client.exec_command(cmd)
				out_ = stdout.read()
				if (out_ is not None) and (out_ <> ''):
					stdout_(host, out_)
				err_ = stderr.read()
				if (err_ is not None) and (err_ <> ''):
					stderr_(host, err_)
		else:
			for host in hosts:
				if host not in self.clients:
					continue
				client = self.clients[host]
				print '[%s][%s] Execute \'%s\'' % (datetime.datetime.now(), host, cmd)
				stdin, stdout, stderr = client.exec_command(cmd)
				out_ = stdout.read()
				if (out_ is not None) and (out_ <> ''):
					stdout_(host, out_)
				err_ = stderr.read()
				if (err_ is not None) and (err_ <> ''):
					stderr_(host, err_)
	
	def upload(self, localFile, remoteFile, all_ = True, *hosts):
		if all_:
			for (host, sftp) in self.sftps.items():
				print '[%s][%s] Beginning to upload file %s' % \
					(datetime.datetime.now(), host, localFile)
				sftp.put(localFile, remoteFile)
				print '[%s][%s] Upload file success %s' % \
					(datetime.datetime.now(), host, localFile)
		else:
			for host in hosts:
				if host not in self.sftps:
					continue
				sftp = self.sftps[host]
				print '[%s][%s] Beginning to upload file %s' % \
					(datetime.datetime.now(), host, localFile)
				sftp.put(localFile, remoteFile)
				print '[%s][%s] Upload file success %s' % \
					(datetime.datetime.now(), host, localFile)

	def close(self):
		for (host, client) in self.clients.items():
			client.close()
		for t in self.transports:
			t.close()

	def __init__(self, cfg):
		self.cfg = cfg
		print 'Beginning initialize'
		self.clients = {}
		self.transports = []
		self.sftps = {}
		for entity in cfg:
			hostname = entity.get('hostname', '')
			port = entity.get('port', 22)
			if port is None:
				port = 22
			in_ipaddr = entity.get('in_ipaddr', '')
			ex_ipaddr = entity.get('ex_ipaddr', '')
			ssh_ipaddr = ex_ipaddr
			if ssh_ipaddr is None or len(ssh_ipaddr) == 0:
				ssh_ipaddr = in_ipaddr
			username = entity.get('username', '')
			password = entity.get('password', '')
			keys_ = entity.get('keys', '')
			keys = None
			if keys_ is not None:
				keys = keys_.split(',')
			
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				client.connect(hostname = ssh_ipaddr, \
						port = port, \
						username = username, \
						password = password)
			except paramiko.BadHostKeyException, e:
				print 'BadHostKeyException[%s]: %s' % (hostname, e)
				return None
			except paramiko.AutenticationException, e:
				print 'AutenticationException[%s]: %s' % (hostname, e)
				return None
			except paramiko.SSHException, e:
				print 'SSHException[%s]: %s' % (hostname, e)
				return None
			self.clients[hostname] = client
			t = paramiko.Transport((ssh_ipaddr, port))
			t.connect(username = username, password = password)
			self.transports.append(t)
			sftp = paramiko.SFTPClient.from_transport(t)
			self.sftps[hostname] = sftp
		print 'Initialize success'
		return None
	
	def array(self, name):
		arr = []
		for _ in self.cfg:
			arr.append(_.get(name, ''))
		return arr

	def haskey(self, key, name):
		arr = []
		for _ in self.cfg:
			if key in _.get('keys', []):
				arr.append(_.get(name))
		return arr


