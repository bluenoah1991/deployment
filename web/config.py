#!/usr/bin/python

import sys, os
sys.path.append('..')

import json
import ConfigParser, string

from common import tool

def LoadClusterType():
	global cluster_type
	global role_type
	f = open('cluster_type.json')
	jstr = f.read()
	js = json.loads(jstr)
	cluster_type = {}
	role_type = {}
	for k, v in js.items():
		name = v.get('name')
		startModule = v.get('startModule')
		stopModule = v.get('stopModule')
		cleanModule = v.get('cleanModule')
		cluster_type[k] = {'name': name, 
				'startModule': startModule, 
				'stopModule': stopModule, 
				'cleanModule': cleanModule}
		roles = v.get('roles')
		for k_, v_ in roles.items():
			role_type[k + '_' + k_] = v_

def GetStartModule(name):
	if not globals().has_key('cluster_type'):
		LoadClusterType()
	obj = cluster_type.get(name)
	return obj.get('startModule')

def GetStopModule(name):
	if not globals().has_key('cluster_type'):
		LoadClusterType()
	obj = cluster_type.get(name)
	return obj.get('stopModule')

def GetCleanModule(name):
	if not globals().has_key('cluster_type'):
		LoadClusterType()
	obj = cluster_type.get(name)
	return obj.get('cleanModule')

def GetClusterType(name):
	if not globals().has_key('cluster_type'):
		LoadClusterType()
	obj = cluster_type.get(name)
	return obj.get('name')

def GetRoleType(name):
	if not globals().has_key('role_type'):
		LoadClusterType()
	return role_type.get(name)

def LoadMachineStatus():
	global machine_status
	f = open('machine_status.json')
	js = f.read()
	machine_status = json.loads(js)

def GetMachineStatus(name):
	if not globals().has_key('machine_status'):
		LoadMachineStatus()
	return machine_status.get(name)

def LoadOSType():
	global os_type
	f = open('os.json')
	js = f.read()
	os_type = json.loads(js)

def GetAllOSType():
	if not globals().has_key('os_type'):
		LoadOSType()
	return os_type

def GetOSType(name):
	if not globals().has_key('os_type'):
		LoadOSType()
	return os_type.get(name)

def LoadMysqlConfig():
	global mysql_host
	global mysql_user
	global mysql_password
	global mysql_database
	cf = ConfigParser.ConfigParser()
	cf.read('web.conf')
	mysql_host = cf.get('mysql', 'host')
	mysql_user = cf.get('mysql', 'user')
	mysql_password = cf.get('mysql', 'password')
	mysql_database = cf.get('mysql', 'database')

def MysqlConnector():
	if not globals().has_key('mysql_host'):
		LoadMysqlConfig()
	if not globals().has_key('mysql_user'):
		LoadMysqlConfig()
	if not globals().has_key('mysql_password'):
		LoadMysqlConfig()
	if not globals().has_key('mysql_database'):
		LoadMysqlConfig()
	host = mysql_host
	user = mysql_user
	password = mysql_password
	database = mysql_database
	con = tool.connect_mysql(
		host = host, 
		user = user, 
		password = password, 
		database = database
		)
	if con is None:
		return None
	connector = tool.Connector(con)
	return connector

def Run():
	LoadClusterType()
	LoadMachineStatus()
	LoadMysqlConfig()
