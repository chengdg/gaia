# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.product.encode_product_service import EncodeProductService
from business.mall.corporation_factory import CorporationFactory


class ACPSPromotedProducts(api_resource.ApiResource):
	"""

	"""
	app = 'product'
	resource = 'cps_promoted_products'

	@param_required(['corp_id', 'product_status'])
	def get(args):
		"""
		:param product_status insale: 在售, forsale: 下架 , pool: 商品池列表
		"""
		corp = args['corp']
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 10))
		})
		filters = json.loads(args.get('filters', '{}'))
		product_status = args.get('product_status')
		# with_product_model: 填充所有商品规格信息
		# with_product_promotion: 填充商品促销信息
		# with_image: 填充商品轮播图信息
		# with_property: 填充商品属性信息
		# with_selected_category: 填充选中的分类信息
		# with_all_category: 填充所有商品分类详情
		# with_sales: 填充商品销售详情
		# with_cps_promotion_info: 填充商品cps推广信息

		if product_status == 'insale':
			insale_shelf = corp.insale_shelf

			products, pageinfo = insale_shelf.search_cps_promoted_products(filters, target_page)
		elif product_status == 'forsale':
			forsale_shelf = corp.forsale_shelf

			products, pageinfo = forsale_shelf.search_cps_promoted_products(filters, target_page)
		else:
			products, pageinfo = corp.product_pool.search_promoted_products(filters, target_page)

		encode_product_service = EncodeProductService.get(corp)

		datas = []
		for product in products:
			base_info = encode_product_service.get_base_info(product)
			models_info = encode_product_service.get_models_info(product)
			supplier = encode_product_service.get_supplier_info(product)
			classifications = encode_product_service.get_classifications(product)
			image_info = encode_product_service.get_image_info(product)
			categories = encode_product_service.get_categories(product)
			cps_promotion_info = encode_product_service.get_cps_promotion_info(product)

			data = {
				"id": product.id,
				"name": base_info['name'],
				"create_type": base_info['create_type'],
				"image": image_info['thumbnails_url'],
				"models_info": models_info,
				"bar_code": base_info['bar_code'],
				"display_index": base_info['display_index'],
				'supplier': supplier,
				'classifications': classifications,
				"categories": categories,
				"sales": base_info['sales'],
				"created_at": base_info['created_at'],
				"sync_at": base_info['sync_at'],
				"display_index": base_info['display_index'],
				'supplier': supplier,
				'classifications': classifications,
				'cps_promotion_info': cps_promotion_info,
			}

			datas.append(data)

		return {
			'pageinfo': pageinfo.to_dict(),
			'products': datas
		}
