# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo

class APreProducts(api_resource.ApiResource):
	"""
	待审核商品集合
	"""
	app = "mall"
	resource = "pre_products"

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		page_info = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 15))
		})
		pageinfo, pre_products = corp.pre_product_repository.filter(args, page_info)

		rows = []

		for pre_product in pre_products:
			rows.append({
				'id': pre_product.id,
				'classification_id': pre_product.classification_id,
				'name': pre_product.name,
				'price': pre_product.price,
				'settlement_price': pre_product.settlement_price,
				'total_sales': 0, #TODO 获取已入库商品的销量
				'stock': pre_product.stock,
				'status_text': pre_product.status_text,
				'status': pre_product.review_status,
				'classification_name_nav': pre_product.classification_nav,
				'is_updated': pre_product.is_updated,
				'is_accepted': pre_product.is_accepted,
				'refuse_reason': pre_product.refuse_reason,
				'remark': pre_product.remark,
				'created_at': pre_product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'images': [], #TODO
				'label_names': [] #TODO 商品标签
			})
		return {
			'rows': rows,
			'pageinfo': pageinfo.to_dict()
		}
		