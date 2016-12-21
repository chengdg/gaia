# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog

from db.mall import promotion_models

from business import model as business_model
from business.product.encode_product_service import EncodeProductService


class EncodePromotionService(business_model.Service):
	"""
	将Promotion对象转换为可输出dict的服务
	"""
	def get_base_info(self, promotion):
		"""
		获取促销的基础信息
		"""
		data = {
			'id': promotion.id,
			'name': promotion.name,
			'promotion_title': promotion.promotion_title,
			'type': promotion.type,
			'type_name': promotion.id,
			'status': promotion.status,
			'start_date': promotion.start_date,
			'end_date': promotion.end_date,
			'member_grade_id': promotion.member_grade_id,
			'created_at': promotion.created_at,
		}

		return data

	def get_products_info(self, promotion):
		"""
		获得促销中的商品信息
		"""
		if promotion.products:
			result = []
			for product in promotion.products:
				encode_product_service = EncodeProductService.get(self.corp)
				base_info = encode_product_service.get_base_info(product)
				models_info = encode_product_service.get_models_info(product)
				supplier = encode_product_service.get_supplier_info(product)
				classifications = encode_product_service.get_classifications(product)
				image_info = encode_product_service.get_image_info(product)
				categories = encode_product_service.get_categories(product)

				data = {
					"id": product.id,
					"name": base_info['name'],
					"create_type": base_info['create_type'],
					"is_member_product": base_info['is_member_product'],
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
				}
				result.append(data)
			return result

	def get_detail_info(self, promotion):
		"""
		获取促销详情信息
		"""

		if promotion.type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
			return self.__get_flash_sale_info(promotion)
		elif promotion.type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			return self.__get_premium_sale_info(promotion)
		elif promotion.type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
			return self.__get_integral_sale_info(promotion)

	def __get_premium_sale_info(self, promotion):
		"""
		获取买赠促销的详细信息
		"""
		if promotion.detail:
			return {
				'count': promotion.detail.count,
				'is_enable_cycle_mode': promotion.detail.is_enable_cycle_mode,
				'premium_products': self.__get_premium_product_info(promotion)
			}

	def __get_flash_sale_info(self, promotion):
		"""
		获取限时抢购促销的详细信息.
		"""
		if promotion.detail:
			return {
				'limit_period': promotion.detail.limit_period,
				'promotion_price': promotion.detail.promotion_price,
				'count_per_purchase': promotion.detail.count_per_purchase,
				'count_per_period': promotion.detail.count_per_period
			}

	def __get_premium_product_info(self, promotion):
		"""
		获取买赠活动中赠送的商品信息
		"""
		premium_products = promotion.detail.premium_products
		datas = []
		for product in premium_products:

			data = {
				'id': product['id'],
				'name': product['name'],
				'thumbnails_url': product['thumbnails_url'],
				'original_premium_count': product['original_premium_count'],
				'premium_count': product['premium_count'],
				'premium_unit': product['premium_unit'],
				'premium_product_id': product['premium_product_id'],
				'supplier': product['supplier'],
				'status': product['status'],
				'is_deleted': product['is_deleted'],
			}
			datas.append(data)
		return datas

	def __get_integral_sale_info(self, promotion):
		detail_info = promotion.detail
		if detail_info:

			is_permanant_active = detail_info.is_permanant_active
			rules = detail_info.rules
			data = {
				'id': detail_info.id,
				'is_permanant_active': is_permanant_active,
				'rules': [
					{
						'id': rule['id'],
						'member_grade_id': rule['member_grade_id'],
						'discount': rule['discount'],
						'discount_money': rule['discount_money'],
					} for rule in rules]

			}
			return data
