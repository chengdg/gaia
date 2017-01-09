# -*- coding: utf-8 -*-
import json

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.mall import models as mall_models

class PreProduct(business_model.Model):
	"""
	待审核商品
	"""
	__slots__ = (
		'is_updated',
		'is_accepted',
		'pending_status',
		'refuse_reason',
		'models'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			self.__init_classification()
			self.__init_models()

	def __init_classification(self):
		db_model = mall_models.ClassificationHasProduct.select().dj_where(product_id=self.id).first()
		self.classification_id = 0 if not db_model else db_model.classification_id

	def __init_models(self):
		"""
		初始化商品规格信息
		"""
		pre_product_models = mall_models.ProductModel.select().dj_where(product_id=self.id, is_deleted=False)
		#商品库存
		if pre_product_models.dj_where(is_standard=False).count() > 0:
			all_model_stocks = [pre_product_model.stocks for pre_product_model in pre_product_models]
			all_model_stocks.sort()
			self.stocks = '{}~{}'.format(all_model_stocks[0], sum(all_model_stocks))
		else:
			self.stocks = pre_product_models.first().stocks

		#商品规格
		pre_product_model_ids = [pre_product_model.id for pre_product_model in pre_product_models]
		property_values = mall_models.ProductModelHasPropertyValue.select().dj_where(model_id__in=pre_product_model_ids)

		property_value_ids = [property_value.property_value_id for property_value in property_values]
		pre_product_model_property_values = mall_models.ProductModelPropertyValue.select().dj_where(id__in=property_value_ids)

		self.models = self.__format_models_data(pre_product_model_property_values)

	def __format_models_data(self, pre_product_model_property_values):
		property_ids = []
		rows = []
		for product_model_property_value in pre_product_model_property_values:
			if product_model_property_value.property_id not in property_ids:
				property_ids.append(product_model_property_value.property_id)
		pre_product_model_properties = mall_models.ProductModelProperty.select().dj_where(id__in=property_ids)

		property_id2model_property_value = {}
		for model_property_value in pre_product_model_property_values:
			if model_property_value.property_id not in property_id2model_property_value:
				property_id2model_property_value[model_property_value.property_id] = [{
					'name': model_property_value.name,
					'pic_url': model_property_value.pic_url,
					'id': model_property_value.id
				}]
			else:
				property_id2model_property_value[model_property_value.property_id].append({
					'name': model_property_value.name,
					'pic_url': model_property_value.pic_url,
					'id': model_property_value.id
				})

		for pre_product_model_property in pre_product_model_properties:
			if pre_product_model_property.id in property_id2model_property_value:
				pre_product_model_value = property_id2model_property_value[pre_product_model_property.id]
				rows.append({
					'id': pre_product_model_property.id,
					'product_model_name': pre_product_model_property.name,
					'model_type': pre_product_model_property.type,
					'product_model_value': '' if not pre_product_model_value else json.dumps(pre_product_model_value),
				})

		return rows

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
		db_models = mall_models.ProductModel.select().dj_where(product_id=self.id, is_standard=False, is_deleted=False)
		return db_models.count() > 0

	@property
	def has_same_postage(self):
		"""
		是否统一运费
		"""
		return self.postage_type == mall_models.POSTAGE_TYPE_UNIFIED