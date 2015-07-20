#!/usr/bin/python

import sys, os
import config
import session
from common import tool


def login(handler):
	_ = handler.request.arguments
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		handler.redirect('/login.html', permanent = True)
		return None
	connector = tool.Connector(con)
		
	uname = _.get('username', None)
	if uname is None or len(uname) == 0:
		handler.redirect('/login.html', permanent = True)
		return None
	db_result = connector.select('u_user', '`uname` = "%s"' % uname[0])
	if len(db_result) == 0:
		handler.redirect('/login.html', permanent = True)
		return None
	raw_password = db_result[0].get('passwd', None)
	if raw_password is None:
		handler.redirect('/login.html', permanent = True)
		return None
	passwd = _.get('password', None)
	if passwd is None or len(passwd) == 0:
		handler.redirect('/login.html', permanent = True)
		return None
	if raw_password <> passwd[0]:
		handler.redirect('/login.html', permanent = True)
		return None
	id_ = db_result[0].get('id', None)
	session.add(handler, id_)
	handler.redirect('/index.html', permanent = True)

