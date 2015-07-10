#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh

if __name__ == '__main__':
	hosts = ssh.init()
	hostnames = []
	for host in hosts:
		hostnames.append(host.get('hostname', ''))
	h_ = ",".join(hostnames)
	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % jdk_tmp_path)
	ssh.upload(hadoop_local_path, hadoop_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % hadoop_tmp_path)
	ssh.upload('hadoop-install.sh', '/tmp/hadoop-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-install.sh')
	ssh.cmd('sudo /tmp/hadoop-install.sh -h %s -t 0' % h_, False, hostnames[0])
	ssh.cmd('sudo /tmp/hadoop-install.sh -h %s -t 1' % h_, False, *hostnames[1:])

