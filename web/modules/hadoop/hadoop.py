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
	ssh.cmd('sudo chmod u+x /tmp/ipconfig-install.sh')
	for _ in cfg:
		hostname = _.get('hostname', '')
		ssh.cmd('sudo /tmp/ipconfig-install.sh -h %s -s %s' % (hostname, pairs), False, hostname)

	jdk_local_path = common.join(__file__, "jdk-8u45-linux-x64.tar.gz")
	jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"
	hadoop_local_path = common.join(__file__, "hadoop-2.6.0.tar.gz")
	hadoop_tmp_path = "/tmp/hadoop-2.6.0.tar.gz"
	spark_local_path = common.join(__file__, "spark-1.3.0-bin-hadoop2.4.tgz")
	spark_tmp_path = "/tmp/spark-1.3.0-bin-hadoop2.4.tgz"

	hostnames = ssh.array('hostname')
	master = ssh.haskey('hadoop_master', 'hostname')
	slave = ssh.haskey('hadoop_slave', 'hostname')
	slave_ = ','.join(slave)

	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % jdk_tmp_path)
	ssh.upload(hadoop_local_path, hadoop_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % hadoop_tmp_path)
	ssh.upload(common.join(__file__, 'hadoop-install.sh'), '/tmp/hadoop-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-install.sh')
	ssh.cmd('sudo /tmp/hadoop-install.sh -m %s -s %s -t 0' % (master[0], slave_), False, *master)
	ssh.cmd('sudo /tmp/hadoop-install.sh -m %s -s %s -t 1' % (master[0], slave_), False, *slave)

	ssh.cmd('sudo /usr/local/hadoop/bin/hdfs namenode -format hadoop', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start namenode', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start datanode', False, *slave)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start resourcemanager', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start nodemanager', False, *slave)

	spark_client = ssh.haskey('spark_client', 'hostname')

	ssh.upload(spark_local_path, spark_tmp_path, False, *spark_client)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % spark_tmp_path, False, *spark_client)
	ssh.upload(common.join(__file__, 'spark-install.sh'), '/tmp/spark-install.sh', False, *spark_client)
	ssh.cmd('sudo chmod u+x /tmp/spark-install.sh', False, *spark_client)
	ssh.cmd('sudo /tmp/spark-install.sh', False, *spark_client)

	ssh.close()
	
def clean(cfg):

	ssh = common.SSH(cfg)
	spark_client = ssh.haskey('spark_client', 'hostname')

	ssh.cmd('sudo rm -rf /usr/local/jdk*')
	ssh.cmd('sudo rm -rf /usr/local/hadoop*')
	ssh.cmd('sudo rm -rf /usr/local/spark*', False, *spark_client)
	ssh.cmd('sudo rm -rf /data')

	ssh.upload(common.join(__file__, 'hadoop-clean.sh'), '/tmp/hadoop-clean.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-clean.sh')
	ssh.cmd('sudo /tmp/hadoop-clean.sh')

	ssh.upload(common.join(__file__, 'ipconfig-clean.sh'), '/tmp/ipconfig-clean.sh')
	ssh.cmd('sudo chmod u+x /tmp/ipconfig-clean.sh')
	ssh.cmd('sudo /tmp/ipconfig-clean.sh')

	ssh.close()

def start(cfg):

	ssh = common.SSH(cfg)
	master = ssh.haskey('hadoop_master', 'hostname')
	slave = ssh.haskey('hadoop_slave', 'hostname')

	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start namenode', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start datanode', False, *slave)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start resourcemanager', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop start nodemanager', False, *slave)

	ssh.close()

def stop(cfg):

	ssh = common.SSH(cfg)
	master = ssh.haskey('hadoop_master', 'hostname')
	slave = ssh.haskey('hadoop_slave', 'hostname')

	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs stop namenode', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs stop datanode', False, *slave)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop stop resourcemanager', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop stop nodemanager', False, *slave)

	ssh.close()
