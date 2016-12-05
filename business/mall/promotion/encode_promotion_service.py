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

	def get_product_info(self, promotion):
		"""
		获得促销中的商品信息
		"""
		product = promotion.product
		if product:
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
			return data

	def get_premium_product_info(self, promotion):
		"""
		获取买赠活动中赠送的商品信息
		"""
		premium_product = promotion.premium_product
		if premium_product:
			encode_product_service = EncodeProductService.get(self.corp)
			base_info = encode_product_service.get_base_info(premium_product)
			models_info = encode_product_service.get_models_info(premium_product)
			supplier = encode_product_service.get_supplier_info(premium_product)
			classifications = encode_product_service.get_classifications(premium_product)
			image_info = encode_product_service.get_image_info(premium_product)
			categories = encode_product_service.get_categories(premium_product)

			data = {
				"id": premium_product.id,
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
			return data

	def get_detail_info(self, promotion):
		"""
		获取促销详情信息
		"""

		if promotion.type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
			pass
		elif promotion.type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			pass

	def __get_premium_sale_info(self, promotion):
		"""
		获取买赠促销的详细信息
		"""
		pass

	def __get_flash_sale_info(self, promotion):
		"""
		获取限时抢购促销的详细信息.
		"""
		pass