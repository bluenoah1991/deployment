#!/usr/bin/python

import sys, os
sys.path.append('..')

import json
import mqtt.client as mqtt

class Unbuffered(object):
	def __init__(self, stream):
		self.stream = stream
	def write(self, data):
		self.stream.write(data)
		self.stream.flush()
	def __getattr__(self, attr):
		return getattr(self.stream, attr)

def refcall(msg):
	if msg is None or len(msg) == 0:
		return None
	if isinstance(msg, basestring):
		msg = json.loads(msg)
	module = msg.get('module')
	if module is None:
		return None
	ns = []
	fullpath = ''
	path = ''
	for i, ch in enumerate(module):
		if ch == '.':
			ns.append((path, fullpath))
			path = ''
		else:
			path = path + ch
		fullpath = fullpath + ch
	ns.append((path, fullpath))
	root = globals().get(ns[0][0])
	if root is None:
		try:
			root = __import__(ns[0][0]) # Import Error
		except ImportError, e:
			return None
	current = root
	for _ in ns[1:]:
		if _[0] not in dir(current):
			try:
				__import__(_[1]) # Import Error
			except ImportError, e:
				return None
		current = getattr(current, _[0])
	if not callable(current):
		return None
	try:
		return current(msg) # Call Failure
	except TypeError, e:
		return None

def background(chdir = False):
	try:
		if os.fork() > 0:
			os._exit(0)
	except OSError, e:
		print 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
		os._exit(1)

	fsock = open('/var/log/deploy.log', 'w')
	fsock2 = open('/dev/null', 'r')
	fsock3 = open('/var/log/deploy.err', 'w')
	sys.stdout = Unbuffered(fsock)
	sys.stdin = fsock2
	sys.stderr = Unbuffered(fsock3)
	if chdir:
		os.chdir('/')
	os.setsid()
	os.umask(0)

# SYS/moduleName
# CLIENT/clientid

def on_connect(client, userdata, flags, rc):
	print('Connected with result code ' + str(rc))
	client.subscribe('SYS/+')

def on_message(client, userdata, msg):
	topic = msg.topic
	if topic.startswith('SYS/'):
		refcall(msg.payload)

if __name__ == '__main__':

	if '-d' in sys.argv:
		background()
	
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect('localhost', 1883, 60)
	client.loop_forever()






