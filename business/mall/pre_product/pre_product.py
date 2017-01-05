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
		'purchase_price',
		'weight',
		'stocks',
		'postage_type',
		'classification_id',
		'limit_zone_type',
		'unified_postage_money',
		'limit_zone',
		'postage_id',
		'is_deleted',
		'is_updated',
		'is_accepted',
		'pending_status',
		'refuse_reason',
		'detail',
		'created_at',
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			self.__init_classification()

	def __init_classification(self):
		db_model = mall_models.ClassificationHasProduct.select().dj_where(product_id=self.id).first()
		self.classification_id = 0 if not db_model else db_model.classification_id

	@property
	def status_text(self):
		"""
		:return: 待入库, 已入库, 入库驳回
		"""
		status_text = u'待入库'
		if self.is_accepted:
			status_text = u'已入库'
		elif self.pending_status == mall_models.PRODUCT_PENDING_STATUS['REFUSED'] and not self.is_accepted:
			status_text = u'入库驳回>>'
		elif self.pending_status == mall_models.PRODUCT_PENDING_STATUS['REFUSED'] and self.is_accepted:
			status_text = u'修改驳回>>'

		return status_text

	@property
	def classification_nav(self):
		"""
		商品分类层级
		"""
		classification_id = self.classification_id
		corp = CorporationFactory.get()
		classifications = corp.product_classification_repository.get_product_classification_tree_by_end(classification_id)
		return '--'.join([classification.name for classification in classifications])

	@property
	def has_multi_models(self):
		"""
		是否多规格
		"""
		db_models = mall_models.ProductModel.select().dj_where(product_id=self.id)
		return db_models.count() > 1

	@property
	def has_same_postage(self):
		"""
		是否统一运费
		"""
		return self.postage_type == mall_models.POSTAGE_TYPE_UNIFIED