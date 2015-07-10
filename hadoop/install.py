#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool
import ipconfig

def main():
	ipconfig.install.main()

	jdk_local_path = tool.join(__file__, "jdk-8u45-linux-x64.tar.gz")
	jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"
	hadoop_local_path = tool.join(__file__, "hadoop-2.6.0.tar.gz")
	hadoop_tmp_path = "/tmp/hadoop-2.6.0.tar.gz"

	hosts = ssh.init()
	hostnames = []
	for host in hosts:
		hostnames.append(host.get('hostname', ''))
	h_ = ",".join(hostnames)

	master = ssh.filterName('hadoop_master', 'hostname')
	slave = ssh.filterName('hadoop_slave', 'hostname')

	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % jdk_tmp_path)
	ssh.upload(hadoop_local_path, hadoop_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % hadoop_tmp_path)
	ssh.upload(tool.join(__file__, 'hadoop-install.sh'), '/tmp/hadoop-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-install.sh')
	ssh.cmd('sudo /tmp/hadoop-install.sh -h %s -t 0' % h_, False, *master)
	ssh.cmd('sudo /tmp/hadoop-install.sh -h %s -t 1' % h_, False, *slave)

if __name__ == '__main__':
	main()
