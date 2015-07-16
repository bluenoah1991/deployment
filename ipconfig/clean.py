#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool

def main(cfg = None):

	if cfg is not None:
		ssh.init2(cfg)

	hosts = ssh.init()
	ssh.upload(tool.join(__file__, 'ipconfig-clean.sh'), '/tmp/ipconfig-clean.sh')
	ssh.cmd('sudo chmod u+x /tmp/ipconfig-clean.sh')
	ssh.cmd('sudo /tmp/ipconfig-clean.sh')


if __name__ == '__main__':
	main()
