#!/usr/bin/python

import sys, os, datetime, json, thread
import paramiko
import select
import mqtt.client as mqtt

class MqttHub(object):
	def __init__(self):
		self.client_ready = set([])
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect('localhost', 1883, 60)
		self.client.loop_start()
	def on_connect(self, client, userdata, flags, rc):
		client.subscribe('sys/client_ready')
	def on_message(self, client, userdata, msg):
		if msg.topic == 'sys/client_ready':
			self.client_ready.add(msg.payload)
			self.client.publish('worker/client_ready/%s' % msg.payload, 'ok')

class MqttClient(object):
	def __init__(self, ttyid):
		self.ready = False
		self.buff = ''
		self.ttyid = ttyid
		self.ready_topic = 'worker/client_ready/%s' % ttyid
		self.webshell_topic = 'webshell/%s' % ttyid
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect('localhost', 1883, 60)
		self.client.loop_start()
	def on_connect(self, client, userdata, flags, rc):
		client.subscribe(self.ready_topic)
	def on_message(self, client, userdata, msg):
		if msg.topic == self.ready_topic and msg.payload == 'ok':
			self.ready = True
			if self.buff is not None and len(self.buff) > 0:
				self.client.publish(self.webshell_topic, self.buff)
	def send(self, message):
		if self.ready:
			self.client.publish(self.webshell_topic, message)
			self.buff += message
		else:
			self.buff += message
	def close(self):
		self.client.disconnect()

class Unbuffered(object):
	def __init__(self, stream):
		self.stream = stream
	def write(self, data):
		self.stream.write(data)
		self.stream.flush()
	def __getattr__(self, attr):
		return getattr(self.stream, attr)

def join(_file_, filename):

	path = os.path.split(os.path.realpath(_file_))[0]
	return os.path.join(path, filename)

class SSH(object):

	def write(self, msg):
		if self.tty:
			sys.stdout.write(msg)
			self.mqttclient.send(msg)
		else:
			sys.stdout.write(msg)

	def cmd(self, cmd, sudo = False, all_ = True, *hosts):
		if all_:
			for (host, channel) in self.channels.items():
				self.write('[%s][%s] Execute \'%s\'\n' % (datetime.datetime.now(), host, cmd))
				if sudo:
					channel.exec_command('sudo -k %s' % cmd)
					channel.send(self.password[host] + '\n')
				else:
					channel.exec_command(cmd)
				while True:
					rl, wl, xl = select.select([channel], [], [], 0.0)
					if len(rl) > 0:
						d = channel.recv(1024)
						if d is None or len(d) == 0:
							break
						self.write(d)
				t = channel.get_transport()
				channel = t.open_session()
				channel.set_combine_stderr(True)
				channel.get_pty()
				self.channels[host] = channel
		else:
			for host in hosts:
				if host not in self.channels:
					continue
				channel = self.channels[host]
				self.write('[%s][%s] Execute \'%s\'\n' % (datetime.datetime.now(), host, cmd))
				if sudo:
					channel.exec_command('sudo -k %s' % cmd)
					channel.send(self.password[host] + '\n')
				else:
					channel.exec_command(cmd)
				while True:
					rl, wl, xl = select.select([channel], [], [], 0.0)
					if len(rl) > 0:
						d = channel.recv(1024)
						if d is None or len(d) == 0:
							break
						self.write(d)
				t = channel.get_transport()
				channel = t.open_session()
				channel.set_combine_stderr(True)
				channel.get_pty()
				self.channels[host] = channel
	
	def upload(self, localFile, remoteFile, all_ = True, *hosts):
		if all_:
			for (host, sftp) in self.sftps.items():
				self.write('[%s][%s] Beginning to upload file %s\n' % \
					(datetime.datetime.now(), host, localFile))
				sftp.put(localFile, remoteFile)
				self.write('[%s][%s] Upload file success %s\n' % \
					(datetime.datetime.now(), host, localFile))
		else:
			for host in hosts:
				if host not in self.sftps:
					continue
				sftp = self.sftps[host]
				self.write('[%s][%s] Beginning to upload file %s\n' % \
					(datetime.datetime.now(), host, localFile))
				sftp.put(localFile, remoteFile)
				self.write('[%s][%s] Upload file success %s\n' % \
					(datetime.datetime.now(), host, localFile))

	def close(self):
		for (host, channel) in self.channels.items():
			channel.close()
		for (host, sftp) in self.sftps.items():
			sftp.close()
		for t in self.transports:
			t.close()
		for (host, client) in self.clients.items():
			client.close()
		if self.tty:
			self.mqttclient.close()

	def __init__(self, cfg, ttyid):
		self.cfg = cfg
		print 'Beginning initialize'
		self.clients = {}
		self.channels = {}
		self.transports = []
		self.sftps = {}
		self.password = {}
		self.tty = False
		if ttyid is not None and len(ttyid) > 0:
			self.tty = True
			self.mqttclient = MqttClient(ttyid)
		for entity in cfg:
			hostname = entity.get('hostname', '')
			port = entity.get('port', '22')
			if port is None or len(port) == 0:
				port = 22
			port = int(port)
			in_ipaddr = entity.get('in_ipaddr', '')
			ex_ipaddr = entity.get('ex_ipaddr', '')
			ssh_ipaddr = ex_ipaddr
			if ssh_ipaddr is None or len(ssh_ipaddr) == 0:
				ssh_ipaddr = in_ipaddr
			username = entity.get('username', '')
			password = entity.get('password', '')
			self.password[hostname] = password
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
			except paramiko.AuthenticationException, e:
				print 'AuthenticationException[%s]: %s' % (hostname, e)
				return None
			except paramiko.SSHException, e:
				print 'SSHException[%s]: %s' % (hostname, e)
				return None
			self.clients[hostname] = client
			t = client.get_transport()
			self.transports.append(t)
			channel = t.open_session()
			channel.set_combine_stderr(True)
			channel.get_pty()
			self.channels[hostname] = channel
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


