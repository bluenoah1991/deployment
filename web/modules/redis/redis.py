#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	ssh = common.SSH(cfg, ttyid)
	ssh.cmd('apt-get update', True)
	ssh.upload(common.join(__file__, 'redis-install.sh'), '/tmp/redis-install.sh')
	ssh.cmd('chmod u+x /tmp/redis-install.sh', True)
	ssh.cmd('/tmp/redis-install.sh', True)
	ssh.close()


