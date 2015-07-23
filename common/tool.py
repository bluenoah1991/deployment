#!/usr/bin/python

import sys, os

def stdout(host, out):
	sys.stdout.write('%s say:\n' % host)
	sys.stdout.write(out)

def stderr(host, out):
	sys.stdout.write('%s say(stderr):\n' % host)
	sys.stdout.write(out)

def join(_file_, filename):
	path = os.path.split(os.path.realpath(_file_))[0]
	return os.path.join(path, filename)

def get_argv(tag, default):
	t = default
	if tag in sys.argv:
		i = sys.argv.index(tag)
		if i and i > 0 and len(sys.argv) > i + 1:
			t = sys.argv[i + 1]
	return t


def connect_mysql(host = '127.0.0.1', user = 'root', password = '123456', database = 'mysql'):
	mysql = None
	try:
		mysql = __import__('mysql.connector') # Import Error
	except ImportError, e:
		return None
	if mysql is not None and mysql.connector is not None:
		try:
			con = mysql.connector.connect(user = user, password = password, 
							host = host, database = database)
			return con
		except mysql.connector.Error, e:
			return None
	return None

class Connector(object):
	def __init__(self, con):
		self.con = con
	def insert(self, tableName, d):
		sql = "INSERT INTO `%s` (" % tableName
		keys = d.keys()
		keys_ = [ '`%s`' % _ for _ in keys]
		sql += ','.join(keys_)
		sql += ') VALUES ('
		keys_wrapper = []
		for k in keys:
			keys_wrapper.append("%%(%s)s" % k)
		sql += ','.join(keys_wrapper)
		sql += ')'
		cursor = self.con.cursor()
		id_ = -1
		try:
			cursor.execute((sql), d)
			id_ = cursor.lastrowid
			self.con.commit()
		except Exception, e:
			self.con.rollback()
		cursor.close()
		return id_

	def delete(self, tableName, id_):
		sql = "DELETE FROM `%s` WHERE `id` = %s" % (tableName, id_)
		cursor = self.con.cursor()
		try:
			cursor.execute((sql))
			self.con.commit()
		except Error, e:
			self.con.rollback()
		cursor.close()

	def update(self, tableName, id_, setstr):
		sql = "UPDATE `%s` SET %s WHERE `id` = %s" % (tableName, setstr, id_)
		cursor = self.con.cursor()
		try:
			cursor.execute((sql))
			self.con.commit()
		except Error, e:
			self.con.rollback()
		cursor.close()

	def select(self, tableName, wherestr):
		sql = "SELECT * FROM `%s` WHERE %s" % (tableName, wherestr)
		cursor = self.con.cursor()
		try:
			cursor.execute((sql))
			columns = cursor.column_names
			rows = cursor.fetchall()
			results = []
			for row in rows:
				results.append(dict(zip(columns, row)))
			return results
		except Error, e:
			return None
		cursor.close()
	
	def select_one(self, tableName, wherestr):
		sql = "SELECT * FROM `%s` WHERE %s LIMIT 0,1" % (tableName, wherestr)
		cursor = self.con.cursor()
		try:
			cursor.execute((sql))
			columns = cursor.column_names
			rows = cursor.fetchall()
			if len(rows) > 0:
				return dict(zip(columns, rows[0]))
			return None
		except Error, e:
			return None
		cursor.close()

	def close(self):
		self.con.close()
		






