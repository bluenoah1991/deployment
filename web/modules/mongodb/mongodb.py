#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	ssh = common.SSH(cfg, ttyid)
	ssh.upload(common.join(__file__, 'mongodb-install.sh'), '/tmp/mongodb-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/mongodb-install.sh')
	ssh.cmd('sudo /tmp/mongodb-install.sh')
	ssh.close()


