#!/usr/bin/python

import sys, os, json, uuid, thread, urlparse
import tornado.ioloop
import tornado.web
from modules import *
from common import Unbuffered, MqttHub

reload(sys)
sys.setdefaultencoding('utf8')

def deamon(chdir = False):
	try:
		if os.fork() > 0:
			os._exit(0)
	except OSError, e:
		print 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
		os._exit(1)

	fsock = open('/var/log/io.log', 'w')
	fsock2 = open('/dev/null', 'r')
	fsock3 = open('/var/log/io.err', 'w')
	sys.stdout = Unbuffered(fsock)
	sys.stdin = fsock2
	sys.stderr = Unbuffered(fsock3)
	if chdir:
		os.chdir('/')
	os.setsid()
	os.umask(0)

class IndexHandler(tornado.web.RequestHandler):
	def load(self):
		if not 'data' in dir(self):
			f = open('data.json', 'r')
			jsonstr = f.read()
			self.data = json.loads(jsonstr)
			f.close()

	def get(self):
		self.load()
		index = self.request.uri
		index = index[index.rfind('/') + 1:]
		if index is None or len(index) == 0:
			index = 1
		index = int(index)
		self.render("html/index.html", icons = self.data[(index - 1) * 24: index * 24])

class ToolHandler(tornado.web.RequestHandler):
	def load(self):
		if not 'platform' in dir(self):
			f = open('platform.json', 'r')
			jsonstr = f.read()
			self.platform = json.loads(jsonstr)
			f.close()

	def get(self):
		self.load()
		index = self.request.uri
		index = index[index.rfind('/tool/') + 6:]
		if index is None or len(index) == 0:
			index = 1
		index = int(index)
		self.render("html/tool.html", icons = self.platform[(index - 1) * 6: index * 6])

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		fileName = urlparse.urlparse(self.request.uri).path
		fileName = fileName[fileName.rfind('/') + 1:]
		self.render("html/%s.html" % fileName)

class AjaxHandler(tornado.web.RequestHandler):
	def post(self, name):
		body = self.request.body
		cfg = json.loads(body)
		uu = str(uuid.uuid1())
		if name == 'hadoop':
			if std:
				Hadoop.install(cfg, uu)
			else:
				thread.start_new_thread(Hadoop.install, (cfg, uu))
		if name == 'mongodb':
			if std:
				Mongodb.install(cfg, uu)
			else:
				thread.start_new_thread(Mongodb.install, (cfg, uu))
		if name == 'redis':
			if std:
				Redis.install(cfg, uu)
			else:
				thread.start_new_thread(Redis.install, (cfg, uu))
		if name == 'postfix':
			if std:
				Postfix.install(cfg, uu)
			else:
				thread.start_new_thread(Postfix.install, (cfg, uu))
		if name == 'lamp':
			if std:
				Lamp.install(cfg, uu)
			else:
				thread.start_new_thread(Lamp.install, (cfg, uu))
		if name == 'riak':
			if std:
				Riak.install(cfg, uu)
			else:
				thread.start_new_thread(Riak.install, (cfg, uu))
		if name == 'mqtt':
			if std:
				Mqtt.install(cfg, uu)
			else:
				thread.start_new_thread(Mqtt.install, (cfg, uu))
		if name == 'mysql':
			if std:
				Mysql.install(cfg, uu)
			else:
				thread.start_new_thread(Mysql.install, (cfg, uu))
		if name == 'tomcat':
			if std:
				Tomcat.install(cfg, uu)
			else:
				thread.start_new_thread(Tomcat.install, (cfg, uu))
		if name == 'zookeeper':
			if std:
				Zookeeper.install(cfg, uu)
			else:
				thread.start_new_thread(Zookeeper.install, (cfg, uu))
		if name == 'kafka':
			if std:
				Kafka.install(cfg, uu)
			else:
				thread.start_new_thread(Kafka.install, (cfg, uu))
		if name == 'hbase':
			if std:
				Hbase.install(cfg, uu)
			else:
				thread.start_new_thread(Hbase.install, (cfg, uu))
		if name == 'mesos':
			if std:
				Mesos.install(cfg, uu)
			else:
				thread.start_new_thread(Mesos.install, (cfg, uu))
		self.write(uu)
		
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
	(r"/", IndexHandler),
	(r"/\d+", IndexHandler),
	(r"/tool", ToolHandler),
	(r"/tool/\d+", ToolHandler),
	(r"/ajax-handler/(\S+)", AjaxHandler),
	(r"/\S+", MainHandler),
], **settings)

if __name__ == "__main__":

	if '-d' in sys.argv:
		deamon()

	if '-std' in sys.argv:
		std = True
	else:
		std = False	

	MqttHub()

	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

