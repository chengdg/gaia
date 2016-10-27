# -*- coding: utf-8 -*-
"""@package business.mall.order_products
订单商品(OrderPdocut)集合

OrderProducts用于构建一组OrderProduct，OrderProducts存在的目的是为了后续优化，以最少的数据库访问次数对商品信息进行批量填充

"""

import json

from eaglet.decorator import param_required

import settings
from business.order.delivery_item_product import DeliveryItemProduct
from db.mall import models as mall_models
from business import model as business_model


class DeliveryItemProductRepository(business_model.Model):
	# __slots__ = (
	# 	'corp'
	# )

	def __init__(self, corp):

		business_model.Model.__init__(self)

		self.corp = corp

	@staticmethod
	@param_required(['corp'])
	def get(args):
		corp = args['corp']

		return DeliveryItemProductRepository(corp)

	def set_products_for_delivery_items(self, delivery_items, with_premium_sale):
		"""
		设置订单的商品，性能攸关
		@param delivery_items:
		@param with_premium_sale:
		@return:
		"""

		# ohs_db_model_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=delivery_item_ids)


		# delivery_item_id2ohs_list = {}
		#
		# for ohs in ohs_db_model_list:
		# 	if ohs.order_id in delivery_item_id2ohs_list:
		# 		delivery_item_id2ohs_list[ohs.order_id].append(ohs)
		# 	else:
		# 		delivery_item_id2ohs_list[ohs.order_id] = [ohs]
		#
		#
		# origin_order_ids = [delivery_item.origin_order_id for delivery_item in delivery_items]
		#
		#
		# origin_ohs_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=origin_order_ids)

		# origin_order_id2ohs = {}
		# for ohs in origin_ohs_list:
		# 	origin_order_id2ohs[ohs.order_id] = ohs
		# 	# if ohs.origin_order_id > 0:
		# 	# 	ohs._origin_order_id = ohs.origin_order_id
		# 	# 	origin_order_id2ohs[ohs.origin_order_id] = ohs
		# 	# else:
		# 	# 	origin_order_id2ohs[ohs.order_id] = ohs
		# 	# 	ohs._origin_order_id = ohs.order_id
		#
		# delivery_item_ohs_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=delivery_items)
		# delivery_item_id2origin_ohs = {}
		# delivery_item_id2delivery_item_ohs = {ohs.order_id:ohs for ohs in delivery_item_ohs_list}
		#
		# for delivery_item_ohs in delivery_item_ohs_list:
		# 	if delivery_item_ohs.origin_order_id > 0:
		# 		delivery_item_ohs.real_origin_order_id = delivery_item_ohs.origin_order_id
		#
		# 	else:
		# 		delivery_item_ohs.real_origin_order_id = delivery_item_ohs.order_id
		#
		# for delivery_item_ohs in delivery_item_ohs_list:
		# 	origin_ohs = origin_order_id2ohs[delivery_item_ohs.real_origin_order_id]
		# 	delivery_item.context['origin_ohs'] = delivery_item_ohs_id2delivery_item[delivery_item_ohs.id] context['origin_ohs']
		# promotion_db_model_list = mall_models.OrderHasPromotion.select().dj_where(order_id__in=origin_order_ids)


		delivery_item_ids = [delivery_item.id for delivery_item in delivery_items]
		ohs_db_model_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=delivery_item_ids)

		product_ids = [p.product_id for p in ohs_db_model_list]

		products = self.corp.product_pool.get_products_by_ids(product_ids,
		                                                      {"with_product_model": True, "with_property": True,
		                                                       "with_model_property_info": True})
		product_id2product = {p.id: p for p in products}

		origin_order_ids = [delivery_item.origin_order_id for delivery_item in delivery_items]

		id2promotion = {r.promotion_id: r for r in
		                mall_models.OrderHasPromotion.select().dj_where(order_id__in=origin_order_ids)}

		# [compatibility]: 兼容apiserver产生的出货单的order_has_prduct时候，total_price和price写入的采购价
		origin_ohs_list = mall_models.OrderHasProduct.select().dj_where(order_id__in=origin_order_ids)

		delivery_item_ohs_id2origin_order_ohs = {}

		for delivery_item_ohs in ohs_db_model_list:
			for origin_ohs in origin_ohs_list:
				if delivery_item_ohs.order_id == origin_ohs.order_id and delivery_item_ohs.product_id == origin_ohs.product_id:
					delivery_item_ohs_id2origin_order_ohs[delivery_item_ohs.id] = origin_ohs
					break

		delivery_item_products = []
		for r in ohs_db_model_list:

			promotion_info = {
				'type': '',
				'integral_money': 0,
				'integral_count': 0,
				'grade_discount_money': 0,
				'promotion_saved_money': 0
			}

			product = product_id2product[r.product_id]

			promotion = id2promotion.get(r.promotion_id, None)
			if promotion:
				db_promotion_result = json.loads(promotion.promotion_result_json)
				# type种类:flash_sale、integral_sale、premium_sale
				promotion_info['type'] = promotion.promotion_type

			delivery_item_product = DeliveryItemProduct()
			delivery_item_product.name = product.name
			delivery_item_product.id = r.product_id
			# delivery_item_product.origin_price = r.total_price / r.number
			# delivery_item_product.sale_price = r.price

			# [compatibility]: 兼容apiserver产生的出货单的order_has_prduct时候，total_price和price写入的采购价
			origin_ohs = delivery_item_ohs_id2origin_order_ohs.get(r.id, r)

			delivery_item_product.origin_price = origin_ohs.total_price / r.number
			delivery_item_product.sale_price = origin_ohs.price

			delivery_item_product.total_origin_price = r.total_price
			delivery_item_product.count = r.number
			delivery_item_product.product_model_name = r.product_model_name
			delivery_item_product.delivery_item_id = r.order_id
			delivery_item_product.context['index'] = r.id

			if r.product_model_name == 'standard':
				delivery_item_product.product_model_name_texts = []
			else:
				for custom_model in product.custom_models:
					if r.product_model_name == custom_model.name:
						delivery_item_product.product_model_name_texts = []
						for value in custom_model.property_values:
							delivery_item_product.product_model_name_texts.append(value['name'])
						break
			delivery_item_product.thumbnails_url = product.thumbnails_url
			delivery_item_product.is_deleted = product.is_deleted

			promotion = id2promotion.get(r.promotion_id, None)
			if promotion and promotion.promotion_type == 'premium_sale':
				# 将premium_product转换为order product

				db_promotion_result_version = db_promotion_result.get('version', '0')

				# 兼容weapp少量遗留订单产生错误数据，使得手机端和后台显示一致
				if not db_promotion_result.get('premium_products'):
					continue
				for premium_product in db_promotion_result['premium_products']:
					premium_delivery_item_product = DeliveryItemProduct()
					premium_delivery_item_product.name = premium_product['name']
					if db_promotion_result_version == settings.PROMOTION_RESULT_VERSION:
						premium_delivery_item_product.count = premium_product['premium_count']
						premium_delivery_item_product.thumbnails_url = '%s%s' % (
							settings.IMAGE_HOST, premium_product['thumbnails_url']) if premium_product[
								                                                           'thumbnails_url'].find(
							'http') == -1 else premium_product['thumbnails_url']
					else:
						premium_delivery_item_product.count = premium_product['count']
						premium_delivery_item_product.thumbnails_url = '%s%s' % (
							settings.IMAGE_HOST, premium_product['thumbnails_url']) if premium_product[
								                                                           'thumbnails_url'].find(
							'http') == -1 else premium_product['thumbnails_url']
					premium_delivery_item_product.id = premium_product['id']

					premium_delivery_item_product.promotion_info = {
						'type': 'premium_sale:premium_product',
						'integral_money': 0,
						'integral_count': 0,
						'grade_discount_money': 0,
						'promotion_saved_money': 0
					}

					premium_delivery_item_product.delivery_item_id = r.order_id
					premium_delivery_item_product.context['index'] = r.id + 1

					premium_delivery_item_product.origin_price = 0
					premium_delivery_item_product.sale_price = 0
					premium_delivery_item_product.total_origin_price = 0
					premium_delivery_item_product.product_model_name_texts = []

					delivery_item_products.append(premium_delivery_item_product)

			# 填充限时抢购金额
			if promotion:
				if promotion.promotion_type == "flash_sale":
					promotion_info['promotion_saved_money'] = db_promotion_result['promotion_saved_money']

				# 填充会员等级价金额
				if r.grade_discounted_money:
					promotion_info['grade_discounted_money'] = r.grade_discounted_money

				# 填充积分应用
				integral_product_info = db_promotion_result.get('integral_product_info')
				if integral_product_info:
					if integral_product_info == str(delivery_item_product.id) + '-' + delivery_item_product.product_model_name:
						promotion_info['integral_money'] = promotion.integral_money
						promotion_info['integral_count'] = promotion.integral_count

			delivery_item_product.promotion_info = promotion_info

			# delivery_item_product_info = {
			# 	'rid': r.id,
			# 	'id': r.product_id,
			# 	'model_name': r.product_model_name,
			# 	'count': r.number,
			# 	'promotion_id': r.promotion_id,
			# 	'price': r.price,
			# 	'total_price': r.total_price,
			# 	'promotion_money': r.promotion_money,
			# 	'discount_money': r.grade_discounted_money,
			# 	'promotion_result': promotion_result,
			# 	'integral_sale_id': r.integral_sale_id,
			# 	'delivery_item_id': r.order_id,
			# 	'db_model': product_db_model
			# }
			#
			# delivery_item_product = DeliveryItemProduct.get({
			# 	'corp': self.corp,
			# 	'product_info': delivery_item_product_info
			# })

			delivery_item_products.append(delivery_item_product)

		delivery_item_id2products = {}

		# 把delivery_item_product分配给相应出货单
		for product in delivery_item_products:
			if product.delivery_item_id in delivery_item_id2products:
				delivery_item_id2products[product.delivery_item_id].append(product)
			else:
				delivery_item_id2products[product.delivery_item_id] = [product]

		for delivery_item in delivery_items:
			delivery_item.products = delivery_item_id2products[delivery_item.id]

			# 排序
			delivery_item.products.sort(lambda x, y: cmp(x.context["index"], y.context["index"]))
