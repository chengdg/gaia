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
		'owner_id',
	)

	def __init__(self, owner_id):
		try:
			super(ProductPool, self).__init__()
			self.owner_id = owner_id
		except BaseException as e:
			print e
			print('********')
			print('--', unicode_full_stack())

	@staticmethod
	@param_required(['owner_id'])
	def get(args):
		return ProductPool(args['owner_id'])

	def add(self, product):
		if self.is_has_product(product.id):
			return False, u'{}已存在于{}的商品池'.format(product.id, self.owner_id)
		mall_models.ProductPool.create(product_id=product.id, woid=self.owner_id)
		return True, ''

	def pop(self, product):
		is_success = mall_models.ProductPool.delete().dj_where(product_id=product.id, woid=self.owner_id).execute()
		print('---',is_success)
		return is_success

	def is_has_product(self, product_id):
		return mall_models.ProductPool.select().dj_where(product_id=product_id, woid=self.owner_id).count() > 0
