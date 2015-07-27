#!/usr/bin/python

import sys, os
sys.path.append('..')

import socket
import session, config
from common import tool

from server import zygote
import json, copy, base64

sockFile = '/tmp/d2'

def send(module, message):
	if message is None:
		message = {}
	else:
		message = copy.deepcopy(message)
	message['module'] = module
	message = json.dumps(message)
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	sock.connect(sockFile)
	sock.send(zygote.pack(message))
	sock.close()

def login(message):
	handler = message.get('handler')
	if handler is None:
		handler.redirect('/login.html', permanent = True)
		return None
	_ = handler.request.arguments
	connector = config.MysqlConnector()
	if connector is None:
		handler.redirect('/login.html', permanent = True)
		return None
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

def get_os_options(message):
	result = config.GetAllOSType()
	return json.dumps(result)

def cfg_dns(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	db_result = connector.select('u_machine', '`uid` = %s' % uinfo.get('id', 0))
	connector.close()
	data = json.dumps(db_result)
	msg = {}
	msg['desc'] = data
	send('modules.ipconfig.clean.main', msg)
	send('modules.ipconfig.install.main', msg)

def hosts(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	db_result = connector.select('u_machine', '`uid` = %s' % uinfo.get('id', 0))
	connector.close()
	for _ in db_result:
		os_ = _.get('os')
		if os_ is not None:
			_['os_'] = config.GetOSType(os_)
		_['roles_'] = '' # TODO
	return json.dumps(db_result)

def host_add(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	data = handler.request.body
	obj = json.loads(data)
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	do = {'uid': uinfo.get('id', 0),
		'name': obj.get('name', ''),
		'in_ipaddr': obj.get('in_ipaddr', ''),
		'ex_ipaddr': obj.get('ex_ipaddr', ''),
		'hostname': obj.get('hostname', ''),
		'os': obj.get('os', ''),
		'uname': obj.get('username', ''),
		'passwd': obj.get('password', '')}
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	connector.insert('u_machine', do)
	connector.close()

def clusters(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	db_result = connector.select('u_cluster', '`uid` = %s' % uinfo.get('id', 0))
	connector.close()
	for _ in db_result:
		type_ = _.get('type')
		if type_ is not None:
			_['type_'] = config.GetClusterType(type_)
		status = _.get('status')
		if status is not None:
			_['status_'] = config.GetMachineStatus(status)
	return json.dumps(db_result)
	
def hs_install(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	body = handler.request.body
	cfg = json.loads(body)
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	uid = uinfo.get('id')
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	db_result = []
	for k, v in cfg.items():
		result = connector.select_one('u_machine', '`uid` = %s and `id` = %s' % (uid, k))
		if result is not None:
			result['keys'] = ','.join(v)
			db_result.append(result)
	connector.close()
	data = {}
	data['uid'] = uid
	data['name'] = 'Unknown' # fill it
	data['desc'] = db_result
	send('modules.hs.install.main', data)

def cluster_start(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	body = handler.request.body
	cfg = json.loads(body)
	id_ = cfg.get('id')
	cluster_type = cfg.get('type')
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	uid = uinfo.get('id')
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	result = connector.select_one('u_cluster', '`uid` = %s and `id` = %s' % (uid, id_))
	connector.close()
	if result is None:
		return ''
	desc = result.get('desc')
	if desc is None:
		return ''
	desc = base64.b64decode(desc)
	data = {}
	data['id'] = id_
	data['desc'] = desc
	send(config.GetStartModule(cluster_type), data)

def cluster_stop(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	body = handler.request.body
	cfg = json.loads(body)
	id_ = cfg.get('id')
	cluster_type = cfg.get('type')
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	uid = uinfo.get('id')
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	result = connector.select_one('u_cluster', '`uid` = %s and `id` = %s' % (uid, id_))
	connector.close()
	if result is None:
		return ''
	desc = result.get('desc')
	if desc is None:
		return ''
	desc = base64.b64decode(desc)
	data = {}
	data['id'] = id_
	data['desc'] = desc
	send(config.GetStopModule(cluster_type), data)

def cluster_clean(message):
	handler = message.get('handler')
	if handler is None:
		return ''
	body = handler.request.body
	cfg = json.loads(body)
	id_ = cfg.get('id')
	cluster_type = cfg.get('type')
	uinfo = session.info(handler)
	if uinfo is None:
		return ''
	uid = uinfo.get('id')
	connector = config.MysqlConnector()
	if connector is None:
		return ''
	result = connector.select_one('u_cluster', '`uid` = %s and `id` = %s' % (uid, id_))
	connector.close()
	if result is None:
		return ''
	desc = result.get('desc')
	if desc is None:
		return ''
	desc = base64.b64decode(desc)
	data = {}
	data['id'] = id_
	data['desc'] = desc
	send(config.GetCleanModule(cluster_type), data)



