#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh

def main(cfg = None):

	if cfg is not None:
		ssh.init2(cfg)

	hosts = ssh.init()

	spark_client = ssh.filterName('spark_client', 'hostname')

	ssh.cmd('sudo rm -rf /usr/local/jdk*')
	ssh.cmd('sudo rm -rf /usr/local/hadoop*')
	ssh.cmd('sudo rm -rf /usr/local/spark*', False, *spark_client)
	ssh.cmd('sudo rm -rf /data')

	ssh.close()

if __name__ == '__main__':
	main()
