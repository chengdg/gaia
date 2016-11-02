# -*- coding: utf-8 -*-
from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.cps.product_promote import ProductPromote
from business.cps.product_promote_repository import ProductPromoteRepository


class AProductPromote(api_resource.ApiResource):
	"""
	优惠券
	"""
	app = 'cps'
	resource = 'product_promote'

	@param_required(['woid', 'product_id', 'promote_money', 'promote_stock', 'promote_time_from', 'promote_time_to'])
	def put(args):

		corp = args['corp']

		product_id = args.get('product_id')
		promote_money = args.get('promote_money')
		promote_stock = args.get('promote_stock')
		promote_time_from = args.get('promote_time_from')
		promote_time_to = args.get('promote_time_to')

		promote_sale_count = args.get('promote_sale_count', 0)
		promote_total_money = args.get('promote_total_money', 0)

		product_promote = ProductPromote.create(corp, product_id, promote_money, promote_stock, promote_time_from,
												promote_time_to, promote_sale_count, promote_total_money)

		if product_promote:
			return {
				'id': product_promote.id
			}
		else:
			return 500, {}

	@param_required(['woid', 'promote_detail_id', 'promote_status', 'promote_sale_count', 'promote_total_money', 'promote_stock'])
	def post(args):

		promote_detail_id = args.get('promote_detail_id')
		promote_status = args.get('promote_status')
		promote_sale_count = args.get('promote_sale_count')
		promote_total_money = args.get('promote_total_money')

		promote_stock = args.get('promote_stock')

		corp = args['corp']
		promote = corp.product_promote_repository.get_product_promote(promote_detail_id)
		promote.update_base_info(promote_status, promote_sale_count, promote_total_money, promote_stock)
		return {}
