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

def info(handler):
	session = get(handler)
	if session is None:
		return None
	id_ = session.get('uid', None)
	if id_ is None:
		return None
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		return None
	connector = tool.Connector(con)
	db_result = connector.select('u_user', '`id` = %s' % id_)
	connector.close()
	if len(db_result) == 0:
		return None
	return db_result[0]


if __name__ == '__main__':
	pass
	# new thread
	# clear expired session
