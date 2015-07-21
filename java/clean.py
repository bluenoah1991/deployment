#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool

def main(cfg = None):

	if cfg is not None:
		ssh.init3(cfg)

	hosts = ssh.init()

	ssh.cmd('sudo rm -rf /usr/local/jdk*')
	ssh.upload(tool.join(__file__, 'jdk-clean.sh'), '/tmp/jdk-clean.sh')
	ssh.cmd('sudo chmod u+x /tmp/jdk-clean.sh')
	ssh.cmd('sudo /tmp/jdk-clean.sh')

	ssh.close()

if __name__ == '__main__':
	main()
