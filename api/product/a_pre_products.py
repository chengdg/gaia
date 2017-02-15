# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.product.global_product_repository import GlobalProductRepository


class APreProducts(api_resource.ApiResource):
	"""
	原始商品集合
	"""
	app = "product"
	resource = "pre_products"

	@param_required(['corp_id'])
	def get(args):

		fill_options = {
			'with_price': True,
			'with_image': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_classification': True,
		}
		page_info = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		pageinfo, pre_products = GlobalProductRepository.get().filter_products(args, page_info, fill_options)

		rows = []

		for pre_product in pre_products:
			rows.append({
				'id': pre_product.id,
				'owner_name': '', #TODO
				'classification_id': pre_product.classification_id,
				'models': {
					'standard_model': pre_product.standard_model,
					'custom_models': pre_product.custom_models
				},
				'has_multi_models': pre_product.has_multi_models,
				'name': pre_product.name,
				'price_info': pre_product.price_info,
				'total_sales': 0, #TODO 获取已入库商品的销量
				'stocks': pre_product.stocks,
				'status': pre_product.status,
				'classification_nav': pre_product.classification_nav,
				'is_updated': pre_product.is_updated,
				'is_accepted': pre_product.is_accepted,
				'refuse_reasons': pre_product.refuse_reasons,
				'detail': pre_product.detail,
				'created_at': pre_product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'images': pre_product.swipe_images,
				'label_names': [] #TODO 商品标签
			})
		return {
			'rows': rows,
			'pageinfo': pageinfo.to_dict()
		}