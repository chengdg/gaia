# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from db.member import models as member_models
from db.account import models as account_models
from db.mall import promotion_models
from business.mall.corporation_factory import CorporationFactory


class WebappConfig(business_model.Model):
	"""
	针对webapp的配置
	"""
	__slots__ = (
		'id',
		'max_product_count', #最大商品数量
		'is_enable_bill', #是否启用发票功能
		'show_product_sales', #在商品列表页显示商品销量
		'show_product_sort', #在商品列表页显示商品排序
		'show_product_search', #在商品列表页显示商品搜索框
		'show_shopping_cart', #在商品列表页开启加入购物车功能
		'order_expired_day' #未付款订单过期时间（单位：小时）
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def __build_update_params(self, args):
		"""
		从args中获取存在于__slots__中的属性
		"""
		update_params = {}
		for slot in self.__slots__:
			if slot in args:
				value = args[slot]
				if value == 'true':
					value = True
				if value == 'false':
					value = False
				update_params[slot] = value

		return update_params

	def update(self, args):
		update_params = self.__build_update_params(args)

		corp = CorporationFactory.get()
		mall_models.MallConfig.update(**update_params).dj_where(owner_id=corp.id).execute()
