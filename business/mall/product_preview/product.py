# -*- coding: utf-8 -*-

from business import model as business_model

class ProductPreview(business_model.Model):
	"""
	需要审核过程的商品
	"""
	__slots__ = (
		'id',
		'owner_id',
		'name',
		'title',
		'price',
		'settlement_price',
		'weight',
		'store',
		'valid_time_from',
		'valid_time_to',
		'limit_settlement_price',
		'has_limit_time',
		'has_product_model',
		'classification_id',
		'limit_zone_type',
		'limit_zone',
		'has_same_postage',
		'postage_money',
		'postage_id',
		'is_update',
		'is_refused',
		'refuse_reason',
		'remark',
		'status',
		'is_deleted',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)