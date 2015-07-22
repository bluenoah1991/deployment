#!/usr/bin/python

import sys, os

import config
from common import tool
import ConfigParser, string
import base64


cf = ConfigParser.ConfigParser()
cf.read('server.conf')
config.mysql_host = cf.get('mysql', 'host')
config.mysql_user = cf.get('mysql', 'user')
config.mysql_password = cf.get('mysql', 'password')
config.mysql_database = cf.get('mysql', 'database')


def cluster_building(uid, clusterName, clusterType, desc):
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(
		host = host, user = user, password = password, database = database)
	if con is None:
		return None
	connector = tool.Connector(con)
	desc = base64.b64encode(desc)
	d = {'uid': uid, 'name': clusterName, 'type': clusterType, 'desc': desc, 'status': 1}
	id_ = connector.insert('u_cluster', d)
	connector.close()
	return id_

def cluster_new(id_):
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(
		host = host, user = user, password = password, database = database)
	if con is None:
		return None
	connector = tool.Connector(con)
	connector.update('u_cluster', id_, '`status` = 2')
	connector.close()

def cluster_ok(id_):
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(
		host = host, user = user, password = password, database = database)
	if con is None:
		return None
	connector = tool.Connector(con)
	connector.update('u_cluster', id_, '`status` = 3')
	connector.close()

def cluster_err(id_):
	host = config.mysql_host
	user = config.mysql_user
	password = config.mysql_password
	database = config.mysql_database
	con = tool.connect_mysql(
		host = host, user = user, password = password, database = database)
	if con is None:
		return None
	connector = tool.Connector(con)
	connector.update('u_cluster', id_, '`status` = 4')
	connector.close()
