#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	zks = cfg.get('zks', '')
	hdfs = cfg.get('hdfs', '')

	cfg = cfg.get('hosts', None)
	ssh = common.SSH(cfg, ttyid)

	#maps = []
	#for _ in cfg:
	#	maps.append(_.get('in_ipaddr', ''))
	#	maps.append(_.get('hostname', ''))
	#pairs = ",".join(maps)
	#ssh.upload(common.join(__file__, 'ipconfig-install.sh'), '/tmp/ipconfig-install.sh')
	#ssh.cmd('chmod u+x /tmp/ipconfig-install.sh', True)
	#for _ in cfg:
	#	hostname = _.get('hostname', '')
	#	ssh.cmd('/tmp/ipconfig-install.sh -h %s -s %s' % (hostname, pairs), True, False, hostname)

	#jdk_local_path = common.join(__file__, "jdk-8u45-linux-x64.tar.gz")
	#jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"

	master = ssh.haskey('hbase_master', 'hostname')
	backup = ssh.haskey('hbase_backup', 'hostname')
	if len(backup) == 1:
		backup_ = backup[0]
	else:
		backup_ = ''
	slaves = ssh.haskey('hbase_slave', 'hostname')
	slave_ = ','.join(slaves)

	#ssh.upload(jdk_local_path, jdk_tmp_path)
	#ssh.cmd('tar zxvf %s -C /usr/local' % jdk_tmp_path, True)
	ssh.upload(common.join(__file__, 'hbase-install.sh'), '/tmp/hbase-install.sh')
	ssh.cmd('chmod u+x /tmp/hbase-install.sh', True)
	ssh.cmd('/tmp/hbase-install.sh -b %s -s %s -z %s -h %s' % (backup_, slave_, zks, hdfs), True)

	ssh.cmd('/usr/local/hbase/bin/start-hbase.sh', True, False, *master)

	ssh.close()


