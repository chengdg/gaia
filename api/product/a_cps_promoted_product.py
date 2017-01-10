# -*- coding: utf-8 -*-
from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.encode_product_service import EncodeProductService


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

		product = corp.product_pool.get_product_by_id(product_id)
		if product:
			product.apply_cps_promotion(money, stock, time_from, time_to, sale_count, total_money)
			encode_product_service = EncodeProductService.get()

			cps_promotion_info = encode_product_service.get_cps_promotion_info(product)
			return {
				'id': product.id,
				'cps_promotion_info': cps_promotion_info
			}
		return 500, {}

	@param_required(['corp_id', 'product_id', 'money', 'stock', 'promotion_id', 'status'])
	def post(args):
		"""
		status 推广状态 PROMOTING: 推广中 PROMOTE_OVER: # 推广结束"

		"""
		product_id = args.get('product_id')
		promotion_id = args.get('promotion_id')
		money = args.get('money')
		stock = args.get('stock')

		status = args.get('status')

		sale_count = args.get('sale_count', 0)
		total_money = args.get('total_money', 0)

		corp = args['corp']
		promoted_product = corp.product_pool.get_product_by_id(product_id)
		promoted_product.update_cps_promotion_info(promotion_id, money, stock, sale_count, total_money, status)

		return {}
