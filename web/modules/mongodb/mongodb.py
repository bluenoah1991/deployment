#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	ssh = common.SSH(cfg, ttyid)
	ssh.cmd('apt-get update', True)
	ssh.upload(common.join(__file__, 'mongodb-install.sh'), '/tmp/mongodb-install.sh')
	ssh.cmd('chmod u+x /tmp/mongodb-install.sh', True)
	ssh.cmd('/tmp/mongodb-install.sh', True)
	ssh.close()


