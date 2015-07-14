#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh

def main(cfg = None):

	if cfg is not None:
		ssh.init2(cfg)

	hosts = ssh.init()

	master = ssh.filterName('hadoop_master', 'hostname')
	slave = ssh.filterName('hadoop_slave', 'hostname')

	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start namenode', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start datanode', False, *slave)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start resourcemanager', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start nodemanager', False, *slave)

	ssh.close()

if __name__ == '__main__':
	main()
