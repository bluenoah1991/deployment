#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh, tool

def main(message):

	desc = message.get('desc')
	if desc is None:
		return None

	hosts = ssh.init(desc)
	ssh.upload(tool.join(__file__, 'ipconfig-clean.sh'), '/tmp/ipconfig-clean.sh')
	ssh.cmd('sudo chmod u+x /tmp/ipconfig-clean.sh')
	ssh.cmd('sudo /tmp/ipconfig-clean.sh')


if __name__ == '__main__':
	main()
