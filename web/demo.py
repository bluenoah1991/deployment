#!/usr/bin/python

import sys, os, json
import modules.hs

if __name__ == '__main__':
	f = open('demo.json', 'r')
	jsonstr = f.read()
	cfg = json.loads(jsonstr)
	modules.hs.install(cfg)
