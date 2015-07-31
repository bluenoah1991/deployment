#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	if len(cfg) == 0:
		return
	cfg1 = cfg[0]

	mysqlpwd = cfg1.get('mysqlpwd', '')
	if mysqlpwd is None or len(mysqlpwd) == 0:
		mysqlpwd = '123456'	

	ssh = common.SSH(cfg, ttyid)
	ssh.upload(common.join(__file__, 'lamp-install.sh'), '/tmp/lamp-install.sh')
	ssh.cmd('chmod u+x /tmp/lamp-install.sh', True)
	ssh.cmd('/tmp/lamp-install.sh -p %s' % mysqlpwd, True)
	ssh.close()


