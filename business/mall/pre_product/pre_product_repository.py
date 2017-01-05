# -*- coding: utf-8 -*-

from eaglet.core import paginator

from business import model as business_model
from business.account.user_profile import UserProfile
from db.mall import models as mall_models
from pre_product import PreProduct

class PreProductRepository(business_model.Service):
	def filter(self, query_dict, page_info):
		db_models = mall_models.Product.select().dj_where(is_deleted=False, is_pre_product=True)

		if query_dict.get('owner_name'):
			pass
		if self.corp.is_weizoom_corp():
			db_models = db_models.where(
				(mall_models.Product.pending_status << [mall_models.PRODUCT_PENDING_STATUS['SUBMIT'], mall_models.PRODUCT_PENDING_STATUS['REFUSED']])
				| (mall_models.Product.is_accepted == True)
			)
		else:
			db_models = db_models.dj_where(owner_id=self.corp.id)


		owner_ids = [p.owner_id for p in db_models]
		owner_id2name = UserProfile.get_user_id_2_username(owner_ids)

		pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)

		PreProducts = []
		for model in db_models:
			pre_product = PreProduct(model)
			setattr(pre_product.__class__, 'owner_name', owner_id2name[model.owner_id])
			PreProducts.append(pre_product)

		return pageinfo, PreProducts

	def get_pre_product(self, product_id):
		db_model = mall_models.Product.select().dj_where(id=product_id, is_deleted=False, is_pre_product=True).get()
		pre_product = PreProduct(db_model)
		# 如果是已审核通过的商品，则获取商品池的库存
		if pre_product.is_accepted:
			pass

		return pre_product

	def get_pre_products(self, product_ids):
		db_models = mall_models.Product.select().dj_where(id__in=product_ids, is_deleted=False, is_pre_product=True)
		return [PreProduct(db_model) for db_model in db_models]