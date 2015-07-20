#!/usr/bin/python

import sys
sys.path.append('..')

import os, socket
from common import tool
from server import zygote

import tornado.ioloop
import tornado.web

import ConfigParser, string
import config, session

sockFile = '/tmp/d2'

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		fileName = self.request.uri
		fileName = fileName[fileName.rfind('/') + 1:]
		if fileName is None or len(fileName) == 0:
			fileName = 'index.html'
		self.render("html/%s" % fileName)

class SessionHandler(tornado.web.RequestHandler):
	def get(self):
		session_ = session.get(self)
		if session_ is None:
			self.redirect('login.html', permanent = True)
			return None
		fileName = self.request.uri
		fileName = fileName[fileName.rfind('/') + 1:]
		if fileName is None or len(fileName) == 0:
			fileName = 'index.html'
		self.render("html/%s" % fileName)

class AjaxHandlerModule(tornado.web.RequestHandler):
	def all_(self, moduleName):
		args = [moduleName, self]
		result = zygote.refcall(args)
		if result is not None:
			self.write(result)
		
	def get(self, moduleName):
		self.all_(moduleName)
	def post(self, moduleName):
		self.all_(moduleName)

class AjaxHandler(tornado.web.RequestHandler):
	def post(self):
		command = None
		body = self.request.body
		headers = self.request.headers
		if 'command' in headers:
			command = headers.get('command')
			message = '%s \'%s\'' % (command, body)	
			sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			sock.connect(sockFile)
			sock.send(zygote.pack(message))
			sock.close()

__PARTS__ = {}
__CACHE__ = True

class PartsHandler(tornado.web.RequestHandler):
	def get(self, partName):
		if partName in __PARTS__:
			self.write(__PARTS__.get(partName))
		else:
			f = open(tool.join(__file__, 'parts/%s.html' % partName), 'r')
			content = f.read()
			if __CACHE__:
				__PARTS__[partName] = content
			f.close()
			self.write(content)

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"cookie_secret": "SAB8LF2sGBflryMb6eXFkX#ou@CNta9V",
}

application = tornado.web.Application([
	(r"/", SessionHandler),
	(r"/login.html", MainHandler),
	(r"/\S+.html", SessionHandler),
	(r"/ajax-handler", AjaxHandler),
	(r"/ajax-handler/(\S+)", AjaxHandlerModule),
	(r"/parts/(\S+)", PartsHandler),
], **settings)

if __name__ == "__main__":

	cf = ConfigParser.ConfigParser()
	cf.read('web.conf')
	config.mysql_host = cf.get('mysql', 'host')
	config.mysql_user = cf.get('mysql', 'user')
	config.mysql_password = cf.get('mysql', 'password')
	config.mysql_database = cf.get('mysql', 'database')

	if '-d' in sys.argv:
		zygote.create()
	if '-nocache' in sys.argv:
		__CACHE__ = False

	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

