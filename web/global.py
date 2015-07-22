#!/usr/bin/python

import sys, os
sys.path.append('..')

import config
import session
import web
from common import tool

import json

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
	connector.close()
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
	return None

def get_os_options(handler):
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		return ""
	connector = tool.Connector(con)
	db_result = connector.select('s_os', '1 = 1')
	connector.close()
	result = '['
	items = []
	for row in db_result:
		items.append('{"id": %s, "name": "%s"}' % (row.get('id', 0), row.get('name', '')))
	result += ','.join(items)
	result += ']'
	return result 

def add_host(handler):
	data = handler.request.body
	obj = json.loads(data)
	uinfo = session.info(handler)
	if uinfo is None:
		return ""
	do = {'uid': uinfo.get('id', 0),
		'name': obj.get('name', ''),
		'in_ipaddr': obj.get('in_ipaddr', ''),
		'ex_ipaddr': obj.get('ex_ipaddr', ''),
		'hostname': obj.get('hostname', ''),
		'os': obj.get('os', ''),
		'uname': obj.get('username', ''),
		'passwd': obj.get('password', '')}
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		return ""
	connector = tool.Connector(con)
	db_result = connector.insert('u_machine', do)
	connector.close()
	
def host_list(handler):
	uinfo = session.info(handler)
	if uinfo is None:
		return ""
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		return ""
	connector = tool.Connector(con)
	db_result = connector.select('v_machine', '`uid` = %s' % uinfo.get('id', 0))
	connector.close()
	result = {'columns': ['id', 'name', 'in_ipaddr', 'ex_ipaddr', 'hostname', 'os']}
	result['rows'] = db_result
	return json.dumps(result)

def cluster_list(handler):
	uinfo = session.info(handler)
	if uinfo is None:
		return ""
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		return ""
	connector = tool.Connector(con)
	db_result = connector.select('u_cluster', '`uid` = %s' % uinfo.get('id', 0))
	connector.close()
	result = {'columns': ['id', 'name', 'type', 'status']}
	result['rows'] = db_result
	return json.dumps(result)
	
def cfg_dns(handler):
	uinfo = session.info(handler)
	if uinfo is None:
		return ""
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		return ""
	connector = tool.Connector(con)
	db_result = connector.select('u_machine', '`uid` = %s' % uinfo.get('id', 0))
	connector.close()
	data = json.dumps(db_result)
	web.SendMessage(handler, 'ipconfig.clean.main', data)
	web.SendMessage(handler, 'ipconfig.install.main', data)

def hdfs_install(handler):
	pass

def develop_01_install(handler):
	body = handler.request.body
	cfg = json.loads(body)
	master_id = cfg.get('master', 0)
	spark_client_ids = cfg.get('spark', [])
	uinfo = session.info(handler)
	if uinfo is None:
		return ""
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(host = host, user = user, password = password, database = database)
	if con is None:
		return ""
	connector = tool.Connector(con)
	db_result = connector.select('v_machine', '`uid` = %s' % uinfo.get('id', 0))
	connector.close()
	for _ in db_result:
		id_ = _.get('id', 0)
		if id_ == master_id:
			_['keys'] = 'hadoop_master'
		else:
			_['keys'] = 'hadoop_slave'
		if id_ in spark_client_ids:
			_['keys'] += ',spark_client'
	data = json.dumps(db_result)
	web.SendMessage(handler, 'hadoop.install.main', data)





