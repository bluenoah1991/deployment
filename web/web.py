#!/usr/bin/python

import os

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		items = ["Item 1", "Item 2", "Item 3"]
		self.render("html/demo.html", title="My title", items=items)

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
	(r"/", MainHandler),
], **settings)

if __name__ == "__main__":
	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

