#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	ssh = common.SSH(cfg, ttyid)
	ssh.upload(common.join(__file__, 'mosquitto-install.sh'), '/tmp/mosquitto-install.sh')
	ssh.cmd('chmod u+x /tmp/mosquitto-install.sh', True)
	ssh.cmd('/tmp/mosquitto-install.sh', True)
	ssh.close()


