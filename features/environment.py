# -*- coding: utf-8 -*-

import os
import sys
import logging

#from db.mall import models as mall_models

path = os.path.abspath(os.path.join('.', '..'))
sys.path.insert(0, path)

import unittest
#from pymongo import Connection
import settings
from features.util import bdd_util
from eaglet.core.cache import utils as cache_utils

#from core.service import celeryconfig


# 临时检测bdd时的数据库是否是本地
# def get_ip(domain):
# 	import socket
# 	ip = socket.gethostbyname(domain)
# 	return ip

if settings.DATABASES['default']['HOST'] != 'db.dev.com':
	raise RuntimeError("Do not run BDD when connect online database")
# else:
# 	ip = get_ip('db.dev.com')
# 	if ip != '127.0.0.1':
# 		raise RuntimeError("Do not run BDD when connect online database")



######################################################################################
# __clear_all_account_data: 清空账号数据
######################################################################################
def __clear_all_account_data():
	pass


######################################################################################
# __clear_all_app_data: 清空应用数据
######################################################################################
clean_modules = []
def __clear_all_app_data():
	"""
	清空应用数据
	"""
	if len(clean_modules) == 0:
		for clean_file in os.listdir('./features/clean'):
			if clean_file.startswith('__'):
				continue

			module_name = 'features.clean.%s' % clean_file[:-3]
			module = __import__(module_name, {}, {}, ['*',])	
			clean_modules.append(module)

	for clean_module in clean_modules:
		clean_module.clean()


def before_all(context):
	# cache_utils.clear_db()
	# __clear_all_account_data()	
	from features.util import account_util
	account_util.create_general_corp('jobs')
	account_util.create_general_corp('nokia')

	account_util.create_general_corp('bill')
	account_util.create_general_corp('tom')

	account_util.create_weizoom_corp('weizoom')

	account_util.create_community('zhouxun', u'周迅')
	account_util.create_community('yangmi', u'杨幂')
	account_util.create_community('yaochen', u'姚晨')
	account_util.create_community('zhaowei', u'赵薇')
	account_util.create_community('bigs', u'大S')


	#创建test case，使用assert
	context.tc = unittest.TestCase('__init__')
	bdd_util.tc = context.tc

	#设置bdd模式
	settings.IS_UNDER_BDD = True
	settings.DUMP_FORMATTED_INNER_ERROR_MSG = True
	settings.DUMP_API_CALL_RESULT = False
	settings.ENABLE_BDD_DUMP_RESPONSE = False
	settings.EAGLET_DISABLE_DUMP_REQ_PARAMS = False

	#设置message broker

	#启动weapp下的bdd server
	#print u'TODO2: 启动weapp下的bdd server'
	logging.warning(u'TODO2: 启动weapp下的bdd server')

	#登录添加App
	#client = bdd_util.login('manager')

	# 让Celery以同步方式运行
	# celeryconfig.CELERY_ALWAYS_EAGER = True



def after_all(context):
	pass


def before_scenario(context, scenario):
	context.scenario = scenario
	__clear_all_app_data()


def after_scenario(context, scenario):
	if hasattr(context, 'client') and context.client:
		context.client.logout()

	if hasattr(context, 'driver') and context.driver:
		print('[after scenario]: close browser driver')
		page_frame = PageFrame(context.driver)
		page_frame.logout()
		context.driver.quit()

	if hasattr(context, 'webapp_driver') and context.driver:
		print('[after scenario]: close webapp browser driver')
		context.webapp_driver.quit()

