#!/usr/bin/python

import sys

def stdout(host, out):
	sys.stdout.write('%s say:' % host)
	sys.stdout.write(out)

def stderr(host, out):
	sys.stdout.write('%s say(stderr):' % host)
	sys.stdout.write(out)
