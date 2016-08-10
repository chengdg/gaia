# -*- coding: utf-8 -*-
"""@package business.auth.access_token
表示Zeus App
"""

#from eaglet.core.cache import utils as cache_util
from eaglet.decorator import param_required
from business import model as business_model
from db.account import models as account_models
import logging

class ZeusApp(business_model.Model):
	"""
	Zeus授权的App
	"""
	__slots__ = (
		'id',
		'name',
		'app_key',
		'app_secret'
		'is_deleted'
	)

	@staticmethod
	@param_required(['id'])
	def get(args):
		"""
		factory方法
		"""
		id = args['id']
		return ZeusApp(id)

		
	def __init__(self, id, model=None):
		business_model.Model.__init__(self)

		self.id = id
		if model:
			# 如果给定的DB model，则用db model初始化
			self._init_slot_from_model(model)
		else:
			model = account_models.ZeusApp.get(id=id)
			self._init_slot_from_model(model)
		return


	@property
	def is_available(self):
		return not self.is_deleted

	@staticmethod
	def get_by_key_secret(app_key, app_secret):
		"""
		通过key和secret获取app信息。如果是None，表名无此app或密码错误
		"""
		try:
			app = account_models.ZeusApp.get(app_key=app_key, app_secret=app_secret)
			return ZeusApp(app.id, app)
		except Exception as e:
			logging.info("Exception: {}".format(e))
		return None
