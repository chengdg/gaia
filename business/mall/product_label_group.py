# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from business.mall.corporation_factory import CorporationFactory
from business import model as business_model
from business.mall.product_label import ProductLabel
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
		创建商品标签分类
		:param args:
		:return:
		"""
		corp_id = CorporationFactory.get().id
		label_group_name = args['name']
		#检查重名
		exist_groups = mall_models.ProductLabelGroup.select().dj_where(name=label_group_name, owner_id=corp_id)
		if len(exist_groups) > 0:
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

	@staticmethod
	@param_required(['id'])
	def delete(args):
		label_group_id = int(args['id'])

		#首先删除此分类下的所有标签
		deleted_labels = mall_models.ProductLabel.select().dj_where(label_group_id=label_group_id)
		deleted_label_ids = [str(l.id) for l in deleted_labels]
		deleted_labels.update(is_deleted=True).execute()
		#再删除分类
		mall_models.ProductLabelGroup.update(is_delete=True).dj_where(id=label_group_id).execute()
		#更新已选择这些被删除标签的商品的信息
		mall_models.ProductHasLabel.select().dj_where(label_id__in=deleted_label_ids).delete()
		#更新已选择这些被删除标签的商品分类的信息
		mall_models.ClassificationHasLabel.select().dj_where(label_id__in=deleted_label_ids).delete()