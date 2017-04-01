# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo

class APreProducts(api_resource.ApiResource):
	"""
	原始商品集合
	"""
	app = "product"
	resource = "pre_products"

	@param_required(['corp_id', '?status'])
	def get(args):
		corp = args['corp']

		fill_options = {
			'with_price': True,
			'with_image': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_classification': True,
			'with_product_label': True if args['corp'].is_weizoom_corp() else False,
			'with_sales': True,
			'with_supplier_info': True,
			'with_shelve_status': True
		}
		page_info = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		pageinfo, pre_products = corp.global_product_repository.filter_products(args, page_info, fill_options)

		rows = []
		for pre_product in pre_products:
			owner_corp_info = pre_product.supplier_info
			labels = sorted(pre_product.labels, lambda x,y: cmp(x.id, y.id))

			rows.append({
				'id': pre_product.id,
				'owner_id': pre_product.owner_id,
				'owner_name': owner_corp_info['company_name'] if owner_corp_info else '',
				'company_name': owner_corp_info['company_name'] if owner_corp_info else '',
				'axe_sales_name': owner_corp_info['axe_sales_name'] if owner_corp_info else '',
				'supplier_settlement_type': owner_corp_info['settlement_type'] if owner_corp_info else 0,
				'supplier_info': pre_product.supplier_info,
				'classification_id': pre_product.classification_id,
				'promotion_title': pre_product.promotion_title,
				'models': {
					'standard_model': pre_product.standard_model,
					'custom_models': pre_product.custom_models
				},
				'has_multi_models': pre_product.has_multi_models,
				'name': pre_product.name,
				'price_info': pre_product.price_info,
				'total_sales': pre_product.sales,
				'stocks': pre_product.stocks,
				'status': pre_product.status,
				'shelve_type': pre_product.shelve_type,
				'classification_nav': pre_product.classification_nav,
				'is_updated': pre_product.is_updated,
				'is_accepted': pre_product.is_accepted,
				'refuse_reasons': pre_product.refuse_reasons,
				'detail': pre_product.detail,
				'created_at': pre_product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'images': pre_product.swipe_images,
				'label_names': [label.name for label in labels]
			})
		return {
			'rows': rows,
			'pageinfo': pageinfo.to_dict()
		}