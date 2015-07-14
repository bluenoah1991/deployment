#!/usr/bin/python

import sys, os

def stdout(host, out):
	sys.stdout.write('%s say:\n' % host)
	sys.stdout.write(out)

def stderr(host, out):
	sys.stdout.write('%s say(stderr):\n' % host)
	sys.stdout.write(out)

def join(_file_, filename):
	path = os.path.split(os.path.realpath(_file_))[0]
	return os.path.join(path, filename)

def get_argv(tag, default):
	t = default
	if tag in sys.argv:
		i = sys.argv.index(tag)
		if i and i > 0 and len(sys.argv) > i + 1:
			t = sys.argv[i + 1]
	return t
