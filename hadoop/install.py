#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh

jdk_local_path = "./jdk-8u45-linux-x64.tar.gz"
jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"
jdk_remote_path = "/usr/local/jdk-8u45-linux-x64.tar.gz"
hadoop_local_path = "./hadoop-2.6.0.tar.gz"
hadoop_tmp_path = "/tmp/hadoop-2.6.0.tar.gz"
hadoop_remote_path = "/usr/local/hadoop-2.6.0.tar.gz"

if __name__ == '__main__':
	ssh.init()
	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('sudo cp %s %s' % (jdk_tmp_path, jdk_remote_path))
	ssh.upload(hadoop_local_path, hadoop_tmp_path)
	ssh.cmd('sudo cp %s %s' % (hadoop_tmp_path, hadoop_remote_path))

