#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	ssh = common.SSH(cfg, ttyid)

	jdk_local_path = common.join(__file__, "jdk-8u45-linux-x64.tar.gz")
	jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"

	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('tar zxvf %s -C /usr/local' % jdk_tmp_path, True)
	ssh.upload(common.join(__file__, 'tomcat-install.sh'), '/tmp/tomcat-install.sh')
	ssh.cmd('chmod u+x /tmp/tomcat-install.sh', True)
	ssh.cmd('/tmp/tomcat-install.sh', True)

	ssh.close()
	
