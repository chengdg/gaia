# -*- coding: utf-8 -*-
"""@package business.mall.product_model
商品规格
"""

import json
from bs4 import BeautifulSoup
import math
from datetime import datetime

from eaglet.decorator import param_required
from eaglet.core.cache import utils as cache_util
from db.mall import models as mall_models
from eaglet.core import watchdog
from business import model as business_model
import settings


class ProductModel(business_model.Model):
	"""
	商品规格
	"""
	__slots__ = (
		'id',
		'is_deleted',
		'name',
		'weight',
		'purchase_price',
		'original_price',
		'market_price',
		'user_code',
		'stock_type',
		'stocks',
		'customized_price',

		#new price info used
		'price',
		'weizoom_purchase_price', #供货商-微众结算价
		'community_purchase_price', #微众-社群结算价
		'community_customized_price',  # 社群修改价
		'gross_profit',
		'gross_profit_rate',

		'property_values',
		'property2value'
	)

	def __init__(self, db_model=None, id2property=None, id2propertyvalue=None):
		business_model.Model.__init__(self)

		if db_model:
			self._init_slot_from_model(db_model)
			self.original_price = db_model.price
			self.weizoom_purchase_price = db_model.purchase_price
			self.community_customized_price = 0
			self.customized_price = 0
			self.community_purchase_price = 0
			self.gross_profit = -1
			self.gross_profit_rate = 0
			self.stock_type = 'unlimit' if db_model.stock_type == mall_models.PRODUCT_STOCK_TYPE_UNLIMIT else 'limit'
			self.stocks = db_model.stocks if db_model.stock_type == mall_models.PRODUCT_STOCK_TYPE_LIMIT else u'无限'

			self.__fill_model_property_info(id2property, id2propertyvalue)

	def is_standard_model(self):
		"""
		判断规格是否是标准规格
		"""
		return self.name == 'standard'

	def __fill_model_property_info(self, id2property, id2propertyvalue):
		'''
		获取model关联的property信息
			model.property_values = [{
				'propertyId': 1,
				'propertyName': '颜色',
				'id': 1,
				'value': '红'
			}, {
				'propertyId': 2,
				'propertyName': '尺寸',
				'id': 3,
				'value': 'S'
			}]

			model.property2value = {
				'颜色': '红',
				'尺寸': 'S'
			}
		'''
		if not id2property:
			return

		if self.name == 'standard':
			self.property2value = None
			self.property_values = None
			return

		#商品规格名的格式为${property1_id}:${value1_id}_${property2_id}:${value2_id}
		ids = self.name.split('_')
		property_values = []
		property2value = {}
		for id in ids:
			# id的格式为${property_id}:${value_id}
			if not ':' in id: #处理异常数据
				continue
			_property_id, _value_id = id.split(':')
			_property = id2property.get(_property_id)
			if not _property: #修复一个未知场景下的问题
				continue
			_value = id2propertyvalue[id]
			property2value[_property['name']] = {
				'id': _value['id'],
				'name': _value['name']
			}
			a_image = _value['image'] if _value['image'] else ''
			property_values.append({
				'property_id': _property['id'],
				'property_name': _property['name'],
				'property_type': _property['type'],
				'id': _value['id'],
				'name': _value['name'],
				'image': '%s%s' % (settings.IMAGE_HOST, a_image) if a_image and a_image.find('http') == -1 else a_image
			})

		self.property_values = property_values
		self.property2value = property2value