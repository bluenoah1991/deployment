#!/usr/bin/python

import sys, os

def list(handler):
	_ = handler.request.arguments
	__ = handler.request.query_arguments
	f = open('./tasks-list-demo.json', 'r')
	return f.read()
