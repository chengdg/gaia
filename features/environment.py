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

######################################################################################
# __create_system_user: 创建系统用户
######################################################################################
def __create_system_user(username):
	pass


def before_all(context):
	# cache_utils.clear_db()
	# __clear_all_account_data()
	# __create_system_user('jobs')
	# __create_system_user('bill')
	# __create_system_user('tom')

	#创建test case，使用assert
	context.tc = unittest.TestCase('__init__')
	bdd_util.tc = context.tc

	#设置bdd模式
	settings.IS_UNDER_BDD = True

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

