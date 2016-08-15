# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business.account.user_profile import UserProfile
from business import model as business_model
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from settings import PANDA_IMAGE_DOMAIN
from services.product_service.task import clear_sync_product_cache


class ProductPool(business_model.Model):
	"""
	新商品池业务逻辑对象
	"""
	__slots__ = (

		'owner_id'
	)

	def __init__(self, owner_id):
		super(ProductPool, self).__init__()
		self.owner_id = owner_id

	@staticmethod
	@param_required(['owner_id'])
	def get(args):
		return ProductPool(args['owner_id'])

	def push(self, product):
		mall_models.ProductPool.create(product_id=product.id, woid=self.owner_id)


	def is_has_product(self,product_id):
		pass