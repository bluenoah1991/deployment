#!/usr/bin/python

import sys, os

import config
from common import tool
import base64, json

def u_cluster(uid, name, type_, desc):
	connector = config.MysqlConnector()
	if connector is None:
		return -1
	if not isinstance(desc, basestring):
		desc = json.dumps(desc)
	desc = base64.b64encode(desc)
	d = {'uid': uid, 'name': name, 'type': type_, 'desc': desc, 'status': 'B'}
	id_ = connector.insert('u_cluster', d)
	connector.close()
	return id_

def u_cluster_update_status(id_, status):
	connector = config.MysqlConnector()
	if connector is None:
		return -1
	connector.update('u_cluster', id_, '`status` = "%s"' % status)
	connector.close()

def u_cluster_remove(id_):
	connector = config.MysqlConnector()
	if connector is None:
		return -1
	connector.delete('u_cluster', id_)
	connector.close()
	
