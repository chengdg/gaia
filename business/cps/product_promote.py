# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from business import model as business_model
from db.mall import models as db_models


class ProductPromote(business_model.Model):
	"""
	商品推广
	"""

	__slots__ = (
		'id',
		'product_id',
		'promote_money',
		'promote_stock',
		'promote_time_from',
		'promote_time_to',

		'promote_sale_count',
		'promote_total_money',
		'product'
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		category = ProductPromote(model)
		return category

	@staticmethod
	def create(corp, product_id, promote_money, promote_stock, promote_time_from,
												promote_time_to, promote_sale_count=0, promote_total_money=0):
		product = db_models.Product.select().dj_where(id=product_id).first()
		if not product or product.owner_id != int(corp.id):
			return None
		if ProductPromote.is_product_promoting(product_id=product_id):
			return None
		promote = db_models.PromoteDetail.create(product_id=product_id,
												 promote_money=promote_money,
												 promote_time_from=promote_time_from,
												 promote_time_to=promote_time_to,
												 promote_sale_count=promote_sale_count,
												 promote_total_money=promote_total_money,
												 promote_stock=promote_stock)
		return ProductPromote.from_model({'db_model': promote})

	@staticmethod
	def is_product_promoting(product_id):
		promotes = db_models.PromoteDetail.select().dj_where(product_id=product_id,
															 promote_status=db_models.PROMOTING)
		if promotes.count() > 0:
			return True
		return False

	def update_base_info(self, promote_status, promote_sale_count, promote_total_money, promote_stock):
		"""

		"""

		db_models.PromoteDetail.update(promote_status=promote_status,
									   promote_sale_count=promote_sale_count,
									   promote_total_money=promote_total_money,
									   promote_stock=promote_stock)\
			.dj_where(id=self.id).execute()
