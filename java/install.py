#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool

def main(cfg = None):

	if cfg is not None:
		ssh.init3()

	hosts = ssh.init()

	jdk_local_path = tool.join(__file__, "jdk-8u45-linux-x64.tar.gz")
	jdk_tmp_path = "/tmp/jdk-8u45-linux-x64.tar.gz"

	ssh.upload(jdk_local_path, jdk_tmp_path)
	ssh.cmd('sudo tar zxvf %s -C /usr/local' % jdk_tmp_path)
	ssh.upload(tool.join(__file__, 'jdk-install.sh'), '/tmp/jdk-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/jdk-install.sh')
	ssh.cmd('sudo /tmp/jdk-install.sh')

	ssh.close()

if __name__ == '__main__':
	main()
