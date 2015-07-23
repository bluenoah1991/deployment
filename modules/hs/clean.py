#!/usr/bin/python

import sys
sys.path.append('../..')

from server import db
from common import ssh, tool

def main(message):

	if message is None:
		return None
	desc = message.get('desc')
	if desc is None:
		return None
	id_ = message.get('id')
	if id_ is None:
		return None

	hosts = ssh.init3(desc)

	spark_client = ssh.filterName('spark_client', 'hostname')

	ssh.cmd('sudo rm -rf /usr/local/jdk*')
	ssh.cmd('sudo rm -rf /usr/local/hadoop*')
	ssh.cmd('sudo rm -rf /usr/local/spark*', False, *spark_client)
	ssh.cmd('sudo rm -rf /data')

	ssh.upload(tool.join(__file__, 'hadoop-clean.sh'), '/tmp/hadoop-clean.sh')
	ssh.cmd('sudo chmod u+x /tmp/hadoop-clean.sh')
	ssh.cmd('sudo /tmp/hadoop-clean.sh')

	ssh.close()
	
	db.u_cluster_remove(id_)

if __name__ == '__main__':
	main()
