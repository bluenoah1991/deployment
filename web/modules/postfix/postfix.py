#!/usr/bin/python

import sys
sys.path.append('..')
import common

def install(cfg, ttyid):

	if len(cfg) == 0:
		return
	cfg1 = cfg[0]

	domain = cfg1.get('domain', '')
	hostname = cfg1.get('hostname', '')
	dbname = cfg1.get('dbname', '')
	if dbname is None or len(dbname) == 0:
		dbname = 'mailserver'
	dbuser = cfg1.get('dbuser', '')
	if dbuser is None or len(dbuser) == 0:
		dbuser = 'admin'
	dbpwd = cfg1.get('dbpwd', '')
	if dbpwd is None or len(dbpwd) == 0:
		dbpwd = '123456'
	upwd = cfg1.get('upwd', '')
	if upwd is None or len(upwd) == 0:
		upwd = '123456'
	master = cfg1.get('master', '')
	if master is None or len(master) == 0:
		master = 'postmaster'
	maildir = cfg1.get('maildir', '')
	if maildir is None or len(maildir) == 0:
		maildir = '/var/mail/vhosts/'
	mysqlpwd = cfg1.get('mysqlpwd', '')
	if mysqlpwd is None or len(mysqlpwd) == 0:
		mysqlpwd = '123456'	

	ssh = common.SSH(cfg, ttyid)
	ssh.cmd('apt-get update', True)
	ssh.upload(common.join(__file__, 'mail-install.sh'), '/tmp/mail-install.sh')
	ssh.cmd('chmod u+x /tmp/mail-install.sh', True)
	ssh.cmd(('/tmp/mail-install.sh -d %s '
	'-h %s -l %s -m %s -n %s '
	'-p %s -a %s -y %s -i %s') % \
	(domain, hostname, dbname, dbuser, dbpwd, \
	upwd, master, mysqlpwd, maildir), True)
	ssh.close()


