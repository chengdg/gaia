# -*- coding: utf-8 -*-

from business import model as business_model
from db.mall import models as mall_models


class PreProductFactory(business_model.Service):
	"""
	待审核商品工厂
	"""

	def create_pre_product(self, args):
		"""
		创建待审核商品
		"""
		db_models = mall_models.PreProduct.select().dj_where(name=args['name'], is_deleted=False)

		if db_models.count() > 0:
			return u'商品名已存在'

		pre_product_model = mall_models.PreProduct.create(
			owner_id = self.corp.id,
			name = args['name'],
			promotion_title = args.get('promotion_title', ''),
			has_product_model = args.get('has_product_model', False),
			price = args.get('price', 0),
			weight = args.get('weight', 0),
			stock = args.get('stock', 0),
			limit_zone_type = args.get('limit_zone_type', 0),
			limit_zone = args.get('limit_zone', 0),
			postage_id = args.get('postage_id', 0),
			postage_money = args.get('postage_money', 0),
			has_same_postage = args.get('has_same_postage', True),
			remark = args.get('remark', '')
		)

		return pre_product_model