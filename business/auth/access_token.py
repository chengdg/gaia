# -*- coding: utf-8 -*-
"""@package business.auth.access_token
Access Token

"""
#from eaglet.core.cache import utils as cache_util
from eaglet.decorator import param_required
from business import model as business_model
from zeus_app import ZeusApp
from db.account import models as account_models
import logging
import hashlib
import time
import datetime
#from eaglet.core import watchdog

AUTH_TOKEN_VALID_IN_MIN = 60*24*30

class AccessToken(business_model.Model):
	"""
	访问权限的biz model
	"""
	__slots__ = (
		'access_token',
		'corp_id',
		'used_count',
		'created_at',
		'expire_time',
		'app',
		#'app',
	)

	@staticmethod
	@param_required(['access_token'])
	def get(args):
		"""
		factory方法
		"""
		db_model = account_models.AccessToken.get(access_token = args['access_token'])
		return AccessToken(db_model)

	def __init__(self, db_model):
		business_model.Model.__init__(self)

		if db_model:
			self._init_slot_from_model(db_model)
		return


	@staticmethod
	@param_required(['app_key', 'app_secret', 'woid'])
	def generate(args):
		"""
		生成access_token
		"""
		#id = args['id']
		# 验证app_key和app_secret
		app_key = args['app_key']
		app_secret = args['app_secret']
		woid = args['woid']
		logging.info("authenticate with app_key:{}, app_secret:{}, woid:{}".format(app_key, app_secret, woid))

		app = ZeusApp.get_by_key_secret(app_key, app_secret)
		if app:
			# 生成AccessToken
			timestamp = int(time.time())
			noncestr = 'weizoom'
			text = "woid={}&timestamp={}&noncestr={}".format(woid, timestamp, noncestr)
			h = hashlib.md5()
			h.update(text)
			access_token = h.hexdigest()

			expire_time = datetime.datetime.now() + datetime.timedelta(minutes=AUTH_TOKEN_VALID_IN_MIN) # 有效期(min)
			# 创建record
			db_model = account_models.AccessToken.create(
				access_token = access_token,
				corp_id = woid,
				used_count = 0,
				expire_time = expire_time,
				app = app.id,
				is_active = True)
			return AccessToken(db_model)
		return None
