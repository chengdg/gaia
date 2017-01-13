# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ARefundingDeliveryItem(api_resource.ApiResource):
	"""
	已支付的订单
	"""
	app = 'order'
	resource = 'refunding_delivery_item'

	@param_required(['delivery_item_id', 'corp'])
	def put(args):
		"""
		支付订单
		@return:
		"""
		corp = args['corp']
		delivery_item_id = args['delivery_item_id']

		cash = float(args.get('cash', 0))
		weizoom_card_money = float(args.get('weizoom_card_money', 0))
		member_card_money = float(args.get('member_card_money', 0))
		coupon_money = float(args.get('coupon_money', 0))

		integral = float(args.get('integral', 0))

		delivery_item_repository = corp.delivery_item_repository
		delivery_item = delivery_item_repository.get_delivery_item(delivery_item_id)
		if delivery_item:
			is_success, msg = delivery_item.apply_for_refunding(corp, cash, weizoom_card_money, member_card_money,
			                                                    coupon_money, integral)
			if is_success:
				return {}
			else:
				return 500, {'msg': msg}
		else:
			return 500, {}
