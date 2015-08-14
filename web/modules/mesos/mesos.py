#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	ssh = common.SSH(cfg, ttyid)
	maps = []
	for _ in cfg:
		maps.append(_.get('in_ipaddr', ''))
		maps.append(_.get('hostname', ''))
	pairs = ",".join(maps)
	ssh.upload(common.join(__file__, 'ipconfig-install.sh'), '/tmp/ipconfig-install.sh')
	ssh.cmd('chmod u+x /tmp/ipconfig-install.sh', True)
	for _ in cfg:
		hostname = _.get('hostname', '')
		ssh.cmd('/tmp/ipconfig-install.sh -h %s -s %s' % (hostname, pairs), True, False, hostname)

	jdk_local_path = common.join(__file__, "jdk-8u45-linux-x64.tar.gz")
	jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"

	master = ssh.haskey('mesos_master', 'hostname')
	slave = ssh.haskey('mesos_slave', 'hostname')

	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('tar zxvf %s -C /usr/local' % jdk_tmp_path, True)
	ssh.upload(common.join(__file__, 'mesos-install.sh'), '/tmp/mesos-install.sh')
	ssh.cmd('chmod u+x /tmp/mesos-install.sh', True)
	ssh.cmd('/tmp/mesos-install.sh -m %s -t 0' % master[0], True, False, *master)
	ssh.cmd('/tmp/mesos-install.sh -m %s -t 1' % master[0], True, False, *slave)

	ssh.close()
	
