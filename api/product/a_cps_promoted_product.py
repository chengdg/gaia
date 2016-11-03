# -*- coding: utf-8 -*-
from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory


class ACPSPromotedProduct(api_resource.ApiResource):
	"""
	cps推广商品
	"""
	app = 'product'
	resource = 'cps_promoted_product'

	@param_required(['corp_id', 'product_id', 'money', 'stock', 'time_from', 'time_to'])
	def put(args):

		corp = args['corp']

		product_id = args.get('product_id')
		money = args.get('money')
		stock = args.get('stock')
		time_from = args.get('time_from')
		time_to = args.get('time_to')

		sale_count = args.get('sale_count', 0)
		total_money = args.get('total_money', 0)

		product_factory = ProductFactory.get(corp=corp)
		cps_promoted_product = product_factory.create_cps_promoted_product({'product_id': product_id,
																			'money': money,
																			'stock': stock,
																			'time_from': time_from,
																			'time_to': time_to,
																			'sale_count': sale_count,
																			'total_money': total_money,
																			})
		return {
			'id': cps_promoted_product.id,
			'promotion_info': {
				'id': cps_promoted_product.cps_promoted_info.id
			}
		}

	@param_required(['corp_id', 'product_id', 'money', 'stock', 'promotion_id'])
	def post(args):

		product_id = args.get('product_id')
		promotion_id = args.get('promotion_id')
		money = args.get('money')
		stock = args.get('stock')

		status = args.get('status')

		sale_count = args.get('sale_count', 0)
		total_money = args.get('total_money', 0)

		corp = args['corp']
		promoted_product = corp.product_pool.get_products_by_ids(product_ids=[product_id])
		promoted_product.update_cps_promotion_info(promotion_id, money, stock, sale_count, total_money, status)

		return {}
