#!/usr/bin/python

import sys
from ConfigParser import ConfigParser

def get_argv(tag, default):
	t = default
	if tag in sys.argv:
		i = sys.argv.index(tag)
		if i and i > 0 and len(sys.argv) > i + 1:
			t = sys.argv[i + 1]
	return t

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'Tidy Deployment CLI Toolkit'
		print ''
		print 'hs\t\t(Apache Hadoop 2.6.0 and Apache Spark 1.3.0)'
		return
	if sys.argv[1] == 'hs':
		
