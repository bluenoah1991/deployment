#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool
import ipconfig.install

def main():
	ipconfig.install.main()

	jdk_local_path = tool.join(__file__, "jdk-8u45-linux-x64.tar.gz")
	jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"
	hadoop_local_path = tool.join(__file__, "hadoop-2.6.0.tar.gz")
	hadoop_tmp_path = "/tmp/hadoop-2.6.0.tar.gz"
	spark_local_path = tool.join(__file__, "spark-1.3.0-bin-hadoop2.4.tgz")
	spark_tmp_path = "/tmp/spark-1.3.0-bin-hadoop2.4.tgz"

	hosts = ssh.init()
	hostnames = []
	for host in hosts:
		hostnames.append(host.get('hostname', ''))

	master = ssh.filterName('hadoop_master', 'hostname')
	slave = ssh.filterName('hadoop_slave', 'hostname')

	m_ = master[0]
	s_ = ','.join(slave)

	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % jdk_tmp_path)
	ssh.upload(hadoop_local_path, hadoop_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % hadoop_tmp_path)
	ssh.upload(tool.join(__file__, 'hadoop-install.sh'), '/tmp/hadoop-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-install.sh')
	ssh.cmd('sudo /tmp/hadoop-install.sh -m %s -s %s -t 0' % (m_, s_), False, *master)
	ssh.cmd('sudo /tmp/hadoop-install.sh -m %s -s %s -t 1' % (m_, s_), False, *slave)

	ssh.cmd('sudo /usr/local/hadoop/bin/hdfs namenode -format hadoop', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start namenode', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start datanode', False, *slave)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start resourcemanager', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start nodemanager', False, *slave)

	spark_client = ssh.filterName('spark_client', 'hostname')

	ssh.upload(spark_local_path, spark_tmp_path, False, *spark_client)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % spark_tmp_path, False, *spark_client)
	ssh.upload(tool.join(__file__, 'spark-install.sh'), '/tmp/spark-install.sh', False, *spark_client)
	ssh.cmd('sudo chmod u+x /tmp/spark-install.sh', False, *spark_client)
	ssh.cmd('sudo /tmp/spark-install.sh', False, *spark_client)

	ssh.close()

if __name__ == '__main__':
	main()
