#!/usr/bin/python

import sys
sys.path.append('../..')

from common import ssh, tool

def main(message):

	desc = message.get('desc')
	if desc is None:
		return None

	hosts = ssh.init3(desc)
	maps = []
	for host in hosts:
		maps.append(host.get('ipaddr', ''))
		maps.append(host.get('hostname', ''))
	s_ = ",".join(maps)
	ssh.upload(tool.join(__file__, 'ipconfig-install.sh'), '/tmp/ipconfig-install.sh')
	ssh.cmd('sudo chmod u+x /tmp/ipconfig-install.sh')
	for host in hosts:
		h_ = host.get('hostname', '')
		ssh.cmd('sudo /tmp/ipconfig-install.sh -h %s -s %s' % (h_, s_), False, h_)


if __name__ == '__main__':
	main()
