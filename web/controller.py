#!/usr/bin/python

import sys, os
sys.path.append('..')

import session, config
from common import tool

import json

def cluster_list(handler):
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
	



