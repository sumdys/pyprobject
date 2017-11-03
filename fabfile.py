#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'He Sheng'

'''
Deployment toolkit.
'''

import os, re


from datetime import datetime
from fabric.api import *

env.user = 'michael'
env.sudo_user = 'root'
env.hosts = ['192.168.1.124']

db_user = 'root'
db_password = ''

_TAB_FILE = 'dist-awesome.tar.gz'

_REMOTE_BASE_TAR = '/tmp/%s' % _TAB_FILE

_REMOTE_BASE_DIR = '/srv/awesome'

def _current_path():
	return os.path.abspath('.')

def _now():
	return datetime.now().strtime('%y-%m-%d_%H.%M.%S')

def backup():
	'''
	Dump entire database on server and backup to local.
	'''
	dt = _now()
	f = 'backup-awesome-%s.sql' % dt
	with cd('/tmp'):
		run('mysqldump --user=%s --password=%s --skip-opt --add-drop-table -- default-character-set=utf8 --quick awesom > %s' % (db_user, db_password, f))
		run('tar -czvf %s.tar.ga %s' % (f, f))
		get('%s.tar.gz' % f,'%s/backup/' % _current_path())
		run('rm -f %s' % f)
		run('rm -f %s.tar.gz' % f)

def build():
	'''
	Build dist package.
	'''
	includes = ['static','templates','transwarp','favicon.ico','.py']
	excludes = ['test','.*','*.pyc','*.pyo']
	local('rm -f dist/%s' % _TAB_FILE)
	with lcd(os.path.join(_current_path(),'www')):
		cmd = ['tar','--dereference','-czvf','../dist/%s' % _TAB_FILE]
		cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
		cmd.extend(includes)
		local(' '.join(cmd))