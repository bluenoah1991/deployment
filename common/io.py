#!/usr/bin/python

import sys

def stdout(host, out):
	sys.stdout.write('%s say:\n' % host)
	sys.stdout.write(out)

def stderr(host, out):
	sys.stdout.write('%s say(stderr):\n' % host)
	sys.stdout.write(out)
