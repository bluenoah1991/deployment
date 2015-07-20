#!/usr/bin/python

import sys, os
import config
from common import tool
import uuid, time

__session_pool__ = {}

def add(handler, uid):
	uu = str(uuid.uuid1())
	__session_pool__[uu] = {'uid': uid, 'datetime': time.time()}
	handler.set_secure_cookie('session_id', uu)
	return uu

def remove(sessionid):
	__session_pool__.pop(sessionid)
	handler.set_secure_cookie('session_id', None)

def get(handler):
	sessionid = handler.get_secure_cookie('session_id')
	session = __session_pool__.get(sessionid, None)
	return session

if __name__ == '__main__':
	pass
	# new thread
	# clear expired session
