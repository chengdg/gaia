# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory

from db.mall import models as mall_models

class ProductLabel(business_model.Model):
	"""
	商品标签
	"""
	__slots__ = (
		'id',
		'name',
		'label_group_id',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['label_group_id:int', 'label_name'])
	def create(args):
		"""
		创建商品标签
		"""
		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		#首先检查是否存在该分组
		label_group_id = args['label_group_id']
		label_group = weizoom_corp.product_label_group_repository.get_label_group(label_group_id)
		if label_group:
			#存在分组，则创建属于该分组的标签
			try:
				new_model = mall_models.ProductLabel.create(
					label_group_id = label_group_id,
					owner_id = weizoom_corp.id,
					name = args['label_name']
				)
				return ProductLabel(new_model)
			except:
				watchdog.alert(u'创建商品标签失败，cause：\n{}'.format(unicode_full_stack()))
				return u'创建失败，请检查是否重名'
		else:
			return u'该分组不存在，可能已被删除'