#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	if len(cfg) == 0:
		return
	cfg1 = cfg[0]
	in_ipaddr = cfg1.get('in_ipaddr', '')

	ssh = common.SSH(cfg, ttyid)
	ssh.cmd('apt-get update', True)
	ssh.upload(common.join(__file__, 'riak-install.sh'), '/tmp/riak-install.sh')
	ssh.cmd('chmod u+x /tmp/riak-install.sh', True)
	ssh.cmd('/tmp/riak-install.sh -i %s' % in_ipaddr, True)
	ssh.close()


