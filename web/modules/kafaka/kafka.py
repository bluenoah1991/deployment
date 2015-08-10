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

	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('tar zxvf %s -C /usr/local' % jdk_tmp_path, True)
	ssh.upload(common.join(__file__, 'zookeeper-install.sh'), '/tmp/zookeeper-install.sh')
	ssh.cmd('chmod u+x /tmp/zookeeper-install.sh', True)

	hostnames = ssh.array('hostname')
	s = ','.join(hostnames)

	for i, _ in enumerate(hostnames):
		ssh.cmd('/tmp/zookeeper-install.sh -s %s -i %d' % (s, i+1), True, False, _)

	ssh.upload(common.join(__file__, 'kafka-install.sh'), '/tmp/kafka-install.sh')
	ssh.cmd('chmod u+x /tmp/kafka-install.sh', True)
	ssh.cmd('/tmp/kafka-install.sh', True)

	ssh.close()

