#!/usr/bin/env python
#-*- coding utf-8 -*-

__author__ = 'He Sheng'

import asyncio,logging

import aiomysql

def log(sql,args = ()):
	logging.info('SQL: %s' % sql)

#connect database confing
@asyncio.coroutine
def create_pool(loop, **kw):
	logging.info('create database connetion pool...')
	global __pool
	__pool = yield from aiomysql.create_pool(
		host = kw.get('host','localhost'),
		port = kw.get('port',3306),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		charset = kw.get('charset','utf-8'),
		autocommit = kw.get('autocommit',true),
		maxsize = kw.get('maxsize', 10),
		minsize = kw.get('minsize', 1),
		loop = loop
	)

#查询数据
@asyncio.coroutine
def select(sql, args, size=None):
	log(sql, args)
	global __pool
	with (yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?','%s'),args or ())
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from cur.close()
		logging.info('rows returned：%s' % len(rs))
		return rs


#要执行INSERT、UPDATE、DELETE语句
@asyncio.coroutine
def execute(sql, args, autocommit=True):
	log(sql)
	with (yield from __pool) as conn:
		if not autocommit:
			yield from conn.begin()
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?','%s'),args)
			affected = cur.rowcount()
			if not autocommit:
				yield from conn.commit()
#			yield from conn.close()
		except BaseException as e:
			if not autocommit:
				yield from conn.rollback()
			raise
		return affected


def create_args_string(num):
	L = []
	for n in range(num):
		L.append('?')
	return ','.join(L)



class Field(object):
	"""docstring for Field"""
	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default

	def __str__(self):
		return '<%s,%s:%s>' % (self.__class__.__name__,self.column_type,self.name)
		