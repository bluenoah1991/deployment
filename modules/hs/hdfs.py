#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool

def install(cfg = None):

	if cfg is not None:
		ssh.init3(cfg)

	hadoop_local_path = tool.join(__file__, "hadoop-2.6.0.tar.gz")
	hadoop_tmp_path = "/tmp/hadoop-2.6.0.tar.gz"

	hosts = ssh.init3(cfg)

	master = ssh.filterName('hdfs_master', 'hostname')
	slave = ssh.filterName('hdfs_slave', 'hostname')

	m_ = master[0]
	s_ = ','.join(slave)

	ssh.upload(hadoop_local_path, hadoop_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % hadoop_tmp_path)
	ssh.upload(tool.join(__file__, 'hdfs-install.sh'), '/tmp/hdfs-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/hdfs-install.sh')
	ssh.cmd('sudo /tmp/hdfs-install.sh -m %s -s %s -t 0' % (m_, s_), False, *master)
	ssh.cmd('sudo /tmp/hdfs-install.sh -m %s -s %s -t 1' % (m_, s_), False, *slave)
	ssh.cmd('sudo /usr/local/hadoop/bin/hdfs namenode -format hadoop', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start namenode', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start datanode', False, *slave)
	ssh.close()

