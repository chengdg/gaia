# -*- coding: utf-8 -*-
"""@package business.demo.data
演示数据
"""
from eaglet.core.cache import utils as cache_util
from eaglet.decorator import param_required
from business import model as business_model

class Data(business_model.Model):
	"""
	演示数据
	"""
	__slots__ = (
		'id',
		'name',
		'age'
	)

	@staticmethod
	@param_required(['id'])
	def get(args):
		"""
		factory方法
		"""
		id = args['id']

		return Data(id)
		
	def __init__(self, id):
		business_model.Model.__init__(self)

		self.id = id
		self.name = 'python'
		self.age = 10
