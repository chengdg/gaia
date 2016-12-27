# -*- coding: utf-8 -*-

from business import model as business_model
from db.mall import models as mall_models

class PendingProduct(business_model.Model):
	"""
	待入库商品
	"""
	__slots__ = (
		'id',
		'owner_id',
		'name',
		'promotion_title',
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
		'postage_money',
		'limit_zone',
		'has_same_postage',
		'postage_id',
		'is_deleted',
		'is_updated',
		'review_status',
		'refuse_reason',
		'remark',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	def get(product_id):
		db_model = mall_models.ProductPendingStock.select().dj_where(id=product_id, is_deleted=False).get()
		return PendingProduct(db_model)

	@staticmethod
	def create(params):
		#首先检查是否有重名商品
		db_models = mall_models.ProductPendingStock.select().dj_where(name=params['name'], is_deleted=False)

		if db_models.count() > 0:
			return None, u'商品名已存在'
		model = mall_models.ProductPendingStock.create(**params)

		return PendingProduct(model), ''

	def get_stock_status_text(self):
		"""
		:return: 待入库, 已入库, 入库驳回
		"""
		status_text = u'待入库'
		if self.review_status == mall_models.PENDING_PRODUCT_STATUS['ACCEPT']:
			status_text = u'已入库'
		elif self.review_status == mall_models.PENDING_PRODUCT_STATUS['REFUSED'] and not self.is_updated:
			status_text = u'入库驳回>>'
		elif self.review_status == mall_models.PENDING_PRODUCT_STATUS['REFUSED'] and self.is_updated:
			status_text = u'修改驳回>>'

		return status_text