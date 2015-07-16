#!/usr/bin/python

import sys
sys.path.append('..')

import os, socket
from server import zygote

import tornado.ioloop
import tornado.web

sockFile = '/tmp/d2'

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("html/index.html")

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

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/ajax-handler", AjaxHandler),
], **settings)

if __name__ == "__main__":
	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

