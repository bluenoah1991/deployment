#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool
import ipconfig.clean

def main(cfg = None):

	if cfg is not None:
		ssh.init2(cfg)

	ipconfig.clean.main(cfg)

	hosts = ssh.init()

	spark_client = ssh.filterName('spark_client', 'hostname')

	ssh.cmd('sudo rm -rf /usr/local/jdk*')
	ssh.cmd('sudo rm -rf /usr/local/hadoop*')
	ssh.cmd('sudo rm -rf /usr/local/spark*', False, *spark_client)
	ssh.cmd('sudo rm -rf /data')

	ssh.upload(tool.join(__file__, 'hadoop-clean.sh'), '/tmp/hadoop-clean.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-clean.sh')
	ssh.cmd('sudo /tmp/hadoop-clean.sh')

	ssh.close()

if __name__ == '__main__':
	main()
