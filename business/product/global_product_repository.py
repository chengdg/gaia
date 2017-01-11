# -*- coding: utf-8 -*-

from eaglet.core import paginator

from business import model as business_model
from business.account.user_profile import UserProfile
from db.mall import models as mall_models
from product import Product

class GlobalProductRepository(business_model.Service):
	def __fill_product_details(self, products, fill_options):
		from business.product.fill_product_detail_service import FillProductDetailService
		FillProductDetailService.get().fill_detail(products, fill_options)

	def filter_products(self, query_dict, page_info, fill_options=None):
		db_models = mall_models.Product.select().dj_where(is_deleted=False)

		if query_dict.get('owner_name'):
			pass
		if query_dict['corp'].is_weizoom_corp():
			db_models = db_models.where(
				(mall_models.Product.pending_status << [mall_models.PRODUCT_PENDING_STATUS['SUBMIT'], mall_models.PRODUCT_PENDING_STATUS['REFUSED']])
				| (mall_models.Product.is_accepted == True)
			)
		else:
			db_models = db_models.dj_where(owner_id=query_dict['corp'].id)


		owner_ids = [p.owner_id for p in db_models]
		owner_id2name = UserProfile.get_user_id_2_username(owner_ids)

		if page_info:
			pageinfo, db_models = paginator.paginate(db_models, page_info.cur_page, page_info.count_per_page)
		else:
			pageinfo = None

		products = []
		for model in db_models:
			pre_product = Product(model)
			setattr(pre_product.__class__, 'owner_name', owner_id2name[model.owner_id])
			products.append(pre_product)

		fill_options = fill_options if fill_options else {}
		self.__fill_product_details(products, fill_options)

		return pageinfo, products

	def get_product(self, product_id, fill_options=None):
		db_model = mall_models.Product.select().dj_where(id=product_id, is_deleted=False).get()
		product_model = Product(db_model)
		fill_options = fill_options if fill_options else {}
		self.__fill_product_details([product_model], fill_options)
		return product_model

	def get_products_by_ids(self, product_ids, fill_options=None):
		fill_options = fill_options if fill_options else {}
		product_models = mall_models.Product.select().dj_where(id__in=product_ids)
		products = [Product(model) for model in product_models]

		self.__fill_product_details(products, fill_options)

		pool_products = mall_models.ProductPool.select().dj_where(product_id__in=product_ids)
		id2product = dict([(product.id, product) for product in products])
		for pool_product in pool_products:
			product = id2product[pool_product.product_id]
			if pool_product.type == mall_models.PP_TYPE_SYNC:
				product.create_type = 'sync'
				product.sync_at = pool_product.sync_at
			else:
				product.create_type = 'create'

		# 按照product_ids中id的顺序对products进行顺序调整
		result = []
		for product_id in product_ids:
			product_id = int(product_id)
			result.append(id2product[product_id])
		return result