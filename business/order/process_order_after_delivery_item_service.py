# -*- coding: utf-8 -*-
"""
根据业务暴露订单、出货单接口
如果用户操作订单，则系统自动完成操作出货单；如果用户操作出货单，则根据业务系统自动操作订单
此处"操作"指会引起订单、出货单状态变化的用户行为
此处"用户"指外部系统，如可能是hermes、panda、pay、快递100回调


消息通知：
订单和出货单分别有消息通知

"""
from business import model as business_model
from db.mall import models as mall_models


class ProcessOrderAfterDeliveryItemService(business_model.Service):
	def process_order(self, delivery_item):
		"""
		当处理的是出货单时，需要决策是否处理以及如何处理订单
		对于db层面有没有出货单的订单，db操作已经在出货单完成，只用发送消息通知
		@param delivery_item:
		@param from_status:
		@param to_status:
		@return:
		"""
		order_id = delivery_item.origin_order_id
		if delivery_item.has_db_record:
			only_send_message = False

			delivery_item_repository = self.corp.delivery_item_repository
			delivery_items = delivery_item_repository.get_delivery_items_by_order_id(order_id)
			delivery_items_status_list = [o.status for o in delivery_items]

			# 获取出货单权重集合
			delivery_item_weights = [mall_models.ORDER_STATUS2DELIVERY_ITEM_WEIGHT[status] for status in
			                         delivery_items_status_list]

			to_status = mall_models.DELIVERY_ITEM_WEIGHT2ORDER_STATUS[min(delivery_item_weights)]
		else:
			only_send_message = True
			to_status = delivery_item.status
		order = self.corp.order_repository.get_order(order_id)

		print 'process-----after---------'
		print order.status

		if order.status != to_status:
			if to_status == mall_models.ORDER_STATUS_SUCCESSED:
				order.finish(self.corp, only_send_message)

			if to_status == mall_models.ORDER_STATUS_PAYED_SHIPED:
				order.ship(self.corp, only_send_message)

			if to_status == mall_models.ORDER_STATUS_REFUNDING:
				order.apply_for_refunding(self.corp, only_send_message)

			if to_status == mall_models.ORDER_STATUS_REFUNDED:
				order.refund(self.corp, only_send_message)
