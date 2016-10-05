# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from business.order.order_repository import OrderRepository
from db.account import models as account_model
from db.mall import models as mall_models

from business.product.product_shelf import ProductShelf
from business.product.product_pool import ProductPool
from business.product.property_template.property_template_repository import PropertyTemplateRepository
from business.product.product_model_property_repository import ProductModelPropertyRepository

from business.mall.category_repository import CategoryRepository
from business.mall.image_group.image_group_repository import ImageGroupRepository
from business.mall.pay.pay_interface_repository import PayInterfaceRepository
from business.mall.logistics.postage_config_repository import PostageConfigRepository
from business.mall.config import Config as MallConfig


class Corporation(business_model.Model):
	"""
	商家
	"""
	__slots__ = (
		'id',
		'name',
		'type',
		'webapp_id'
	)

	def __init__(self, owner_id):
		self.id = owner_id
		self.name = 'unknown'
		if owner_id:
			_account_user_profile = account_model.UserProfile.select().dj_where(user_id=owner_id).first()
			self.webapp_id = _account_user_profile.webapp_id
			self.type = _account_user_profile.webapp_type  # todo 数字123到类型名称转换
		else:
			self.webapp_id = 0
			self.type = 0

	@property
	def insale_shelf(self):
		product_shelf = ProductShelf.get({
			"corp": self,
			'type': 'in_sale'
		})

		return product_shelf

	@property
	def forsale_shelf(self):
		product_shelf = ProductShelf.get({
			"corp": self,
			'type': 'for_sale'
		})

		return product_shelf

	@property
	def product_pool(self):
		return ProductPool.get_for_corp({
			"corp": self
		})

	@property
	def category_repository(self):
		return CategoryRepository.get(self)

	@property
	def image_group_repository(self):
		return ImageGroupRepository.get(self)

	@property
	def product_property_template_repository(self):
		return PropertyTemplateRepository.get(self)

	@property
	def product_model_property_repository(self):
		return ProductModelPropertyRepository.get(self)

	@property
	def order_repository(self):
		return OrderRepository.get({'corp': self})

	@property
	def mall_config(self):
		return MallConfig(self)

	@property
	def pay_interface_repository(self):
		return PayInterfaceRepository(self)

	@property
	def postage_config_repository(self):
		return PostageConfigRepository(self)
