#!/usr/bin/python

import sys
sys.path.append('..')

from common import ssh

def main():
	hosts = ssh.init()
	maps = []
	for host in hosts:
		maps.append(host.get('ipaddr', ''))
		maps.append(host.get('hostname', ''))
	s_ = ",".join(maps)
	ssh.upload('ipconfig-install.sh', '/tmp/ipconfig-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/ipconfig-install.sh')
	ssh.cmd('sudo /tmp/ipconfig-install.sh -s %s' % s_)


if __name__ == '__main__':
	main()
