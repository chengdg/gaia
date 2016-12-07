# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from business.mall.corporation_factory import CorporationFactory
from business import model as business_model
from business.mall.label.product_label import ProductLabel
from db.mall import models as mall_models

class ProductLabelGroup(business_model.Model):
	"""
	商品标签
	"""
	__slots__ = (
		'id',
		'name',
		'labels',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)

	def get_labels(self):
		label_models = mall_models.ProductLabel.select().dj_where(label_group_id=self.id, is_deleted=False)
		labels = []
		for model in label_models:
			labels.append(ProductLabel(model))
		return labels

	@staticmethod
	@param_required(['name'])
	def create(args):
		"""
		创建商品标签分组
		:param args:
		:return:
		"""
		corp_id = CorporationFactory.get_weizoom_corporation().id
		label_group_name = args['name']
		#检查重名
		exist_groups = mall_models.ProductLabelGroup.select().dj_where(name=label_group_name, owner_id=corp_id)
		if exist_groups.count() > 0:
			return u'商品标签分类已存在'
		try:
			model = mall_models.ProductLabelGroup.create(
				owner_id = corp_id,
				name = label_group_name
			)
			return ProductLabelGroup(model)
		except:
			watchdog.alert(u'创建商品标签分类失败，cause: \n{}'.format(unicode_full_stack()))
			return u'创建商品标签分类失败'

