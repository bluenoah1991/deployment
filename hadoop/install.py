#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh

jdk_local_path = "./jdk-8u45-linux-x64.tar.gz"
jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"
hadoop_local_path = "./hadoop-2.6.0.tar.gz"
hadoop_tmp_path = "/tmp/hadoop-2.6.0.tar.gz"

if __name__ == '__main__':
	hosts = ssh.init()
	ipaddrs = []
	for host in hosts:
		ipaddrs.append(host.get('ipaddr', ''))
	h_ = ",".join(ipaddrs)
	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % jdk_tmp_path)
	ssh.upload(hadoop_local_path, hadoop_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % hadoop_tmp_path)
	ssh.upload('hadoop-install.sh', '/tmp/hadoop-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-install.sh')
	ssh.cmd('sudo /tmp/hadoop-install.sh -h %s -t 0' % h_, False, ipaddrs[0])
	ssh.cmd('sudo /tmp/hadoop-install.sh -h %s -t 1' % h_, False, *ipaddrs[1:])

