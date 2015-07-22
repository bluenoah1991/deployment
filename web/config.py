#!/usr/bin/python

import sys, os
import json
import ConfigParser, string

def LoadClusterType():
	global cluster_type
	global role_type
	f = open('cluster_type.json')
	js = f.read()
	cluster_type = {}
	role_type = {}
	for k, v in js:
		name = v.get('name')
		cluster_type[k] = name
		roles = v.get('roles')
		for k_, v_ in roles:
			role_type[k + '_' + k_] = v_

def GetClusterType(name):
	return cluster_type.get(name)

def GetRoleType(name):
	return role_type.get(name)

def LoadMachineStatus():
	global machine_status
	f = open('machine_status.json')
	js = f.read()
	machine_status = json.loads(js)

def GetMachineStatus(name):
	return machine_status.get(name)

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
