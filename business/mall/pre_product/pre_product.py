# -*- coding: utf-8 -*-

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.mall import models as mall_models

class PreProduct(business_model.Model):
	"""
	待审核商品
	"""
	__slots__ = (
		'id',
		'name',
		'promotion_title',
		'price',
		'settlement_price',
		'weight',
		'stock',
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
		'is_accepted',
		'review_status',
		'refuse_reason',
		'remark',
		'created_at',
		'mall_product_id'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@property
	def status_text(self):
		"""
		:return: 待入库, 已入库, 入库驳回
		"""
		status_text = u'待入库'
		if self.is_accepted:
			status_text = u'已入库'
		elif self.review_status == mall_models.PRE_PRODUCT_STATUS['REFUSED'] and not self.is_accepted:
			status_text = u'入库驳回>>'
		elif self.review_status == mall_models.PRE_PRODUCT_STATUS['REFUSED'] and self.is_accepted:
			status_text = u'修改驳回>>'

		return status_text

	@property
	def classification_nav(self):
		"""
		商品分类层级
		:return:
		"""
		classification_id = self.classification_id
		corp = CorporationFactory.get()
		classifications = corp.product_classification_repository.get_product_classification_tree_by_end(classification_id)
		return '--'.join([classification.name for classification in classifications])