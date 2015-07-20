#!/usr/bin/python

import sys
sys.path.append('..')

import os, socket
from common import tool
from server import zygote

import tornado.ioloop
import tornado.web

sockFile = '/tmp/d2'

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("html/index.html")

class AjaxHandlerModule(tornado.web.RequestHandler):
	def all_(self, moduleName):
		args = [moduleName, self.request]
		self.write(zygote.refcall(args))
		
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

class PartsHandler(tornado.web.RequestHandler):
	def get(self, partName):
		if partName in __PARTS__:
			self.write(__PARTS__.get(partName))
		else:
			f = open(tool.join(__file__, 'parts/%s.html' % partName), 'r')
			content = f.read()
			__PARTS__[partName] = content
			f.close()
			self.write(content)

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/ajax-handler", AjaxHandler),
	(r"/ajax-handler/(\S+)", AjaxHandlerModule),
	(r"/parts/(\S+)", PartsHandler),
], **settings)

if __name__ == "__main__":

	if '-d' in sys.argv:
		zygote.create()

	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

