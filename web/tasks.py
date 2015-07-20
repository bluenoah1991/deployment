#!/usr/bin/python

import sys, os

def list(request):
	_ = request.arguments
	__ = request.query_arguments
	f = open('./tasks-list-demo.json', 'r')
	return f.read()
