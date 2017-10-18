#!/usr/bin/env python3
# -*- coding utf-8 -*-

'''
Default configurations.
'''

__author__ = 'He Sheng'

configs = {
	'debug':True,
	'db':{
		'host': '127.0.0.1',
		'port': 3306,
		'user': 'www',
		'passport': '',
		'db': 'awesome'
	},
	'session': {
		'secret': 'Awesome'
	}
}