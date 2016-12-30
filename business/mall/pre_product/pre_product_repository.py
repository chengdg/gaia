# -*- coding: utf-8 -*-

from eaglet.core import paginator

from business import model as business_model
from db.mall import models as mall_models
from pre_product import PreProduct

class PreProductRepository(business_model.Service):
	def filter(self, query_dict, page_info):
		query = {
			'is_deleted': False
		}
		if query_dict.get('customer_name'):
			pass
		if self.corp.is_weizoom_corp:
			query['review_status'] = mall_models.PRE_PRODUCT_STATUS['SUBMIT']
		else:
			query['owner_id'] = self.corp.id
		db_models = mall_models.PreProduct.select().dj_where(**query)

		pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)

		return pageinfo, [PreProduct(model) for model in db_models]

	def get_pre_product(self, product_id):
		db_model = mall_models.PreProduct.select().dj_where(id=product_id, is_deleted=False).get()
		pre_product = PreProduct(db_model)
		# 如果是已审核通过的商品，则获取商品池的库存
		if pre_product.is_accepted:
			pass

		return pre_product

	def get_pre_products(self, product_ids):
		db_models = mall_models.PreProduct.select().dj_where(id__in=product_ids, is_deleted=False)
		return [PreProduct(db_model) for db_model in db_models]