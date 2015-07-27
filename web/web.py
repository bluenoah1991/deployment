#!/usr/bin/python

import sys, os, json
import tornado.ioloop
import tornado.web
import modules.hs

def deamon(chdir = False):
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

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		fileName = self.request.uri
		fileName = fileName[fileName.rfind('/') + 1:]
		if fileName is None or len(fileName) == 0:
			fileName = 'index'
		self.render("html/%s.html" % fileName)

class AjaxHandler(tornado.web.RequestHandler):
	def post(self, name):
		if name == 'hs/install':
			body = self.request.body
			cfg = json.loads(body)
			modules.hs.install(cfg)
		
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/\S+.html", MainHandler),
	(r"/ajax-handler/(\S+)", AjaxHandler),
], **settings)

if __name__ == "__main__":

	if '-d' in sys.argv:
		deamon()

	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

