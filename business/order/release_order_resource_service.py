# -*- coding: utf-8 -*-
"""


"""
from eaglet.utils.resource_client import Resource

from business import model as business_model
from business.account.integral import Integral
from db.mall import models as mall_models
from db.member import models as member_models


class ReleaseOrderResourceService(business_model.Service):
	def release(self, order_id,from_status,to_status):
		"""
		当处理的是出货单时，需要决策是否处理以及如何处理订单
		对于db层面有没有出货单的订单，db操作已经在出货单完成，只用发送消息通知
		@param order_id:
		@param from_status:
		@param to_status:
		@return:
		"""

		fill_options = {
			'with_member': True,
			'with_weizoom_card': True,
			'with_delivery_items': {
				'with_products': True,
			}

		}
		corp = self.corp
		order = corp.order_repository.get_order(order_id, fill_options)

		is_paid = (mall_models.MEANINGFUL_WORD2ORDER_STATUS[from_status] != mall_models.ORDER_STATUS_NOT)  # 已经支付过的订单，已增加过销量

		delivery_item_products = order.get_all_products()
		product_ids = [p.id for p in delivery_item_products]
		product_id2delivery_item_product = {p.id: p for p in delivery_item_products}

		products = corp.product_pool.get_products_by_ids(product_ids)
		#
		# for delivery_item_product in delivery_item_products:
		# 	product = corp.product_pool.get_products_by_ids([delivery_item_product.id])[0]
		#
		# 	product.update_sales(delivery_item_product.count)

		for product in products:
			delivery_item_product = product_id2delivery_item_product[product.id]

			# 更新销量库存
			product.update_stock(delivery_item_product.product_model_name, delivery_item_product.count)

			# 更新销量
			if is_paid:
				product.update_sales(0 - delivery_item_product.count)

		# 退款微众卡
		if order.weizoom_card_money:
			trade_id = order.weizoom_card_info['trade_id']
			data = {
				'trade_id': trade_id,
				'trade_type': 1  # 普通退款
			}
			resp = Resource.use('card_apiserver').delete({
				'resource': 'card.trade',
				'data': data
			})

		# 退还优惠券
		if order.coupon_id:
			coupon = corp.coupon_repository.get_coupon_by_id(order.coupon_id)
			if coupon:
				coupon.refund(order)

		# 退还积分
		if order.integral:
			Integral.increase_member_integral({
				'integral_increase_count': order.integral,
				'webapp_user_id': order.webapp_user_id,
				'member_id': order.member_info['id'],
				'event_type': member_models.RETURN_BY_SYSTEM,
				'corp': corp,
			})
